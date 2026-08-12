"""FastAPI service for Cooperative Education AI, powered by OpenTyphoon."""
import json
import os
import re
import warnings
from pathlib import Path
from typing import Optional

warnings.filterwarnings("ignore")

import httpx
from fastapi import FastAPI, File, Form, Header, HTTPException, UploadFile
from openai import OpenAI

import tempfile

BASE_DIR = Path(__file__).resolve().parent

try:
    import mysql.connector
except ImportError:
    mysql = None

try:
    from typhoon_ocr import ocr_document
except ImportError:
    ocr_document = None


def load_env() -> None:
    """Load local variables only when the process environment does not set them."""
    env_path = BASE_DIR / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


load_env()
TYPHOON_API_KEY = os.environ.get("TYPHOON_API_KEY", "")
if TYPHOON_API_KEY:
    os.environ.setdefault("TYPHOON_OCR_API_KEY", TYPHOON_API_KEY)
    client = OpenAI(api_key=TYPHOON_API_KEY, base_url="https://api.opentyphoon.ai/v1")
else:
    client = None

MODEL = os.environ.get("TYPHOON_MODEL", "typhoon-v2.5-30b-a3b-instruct")
SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Coop AI Service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
SERVICE_TOKEN = os.environ.get("AI_SERVICE_TOKEN", "")


def verify_token(authorization: Optional[str]) -> None:
    if SERVICE_TOKEN and authorization != f"Bearer {SERVICE_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")


def db_connection():
    if mysql is None or not hasattr(mysql, "connector"):
        raise HTTPException(status_code=500, detail="mysql-connector-python module is not installed")
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", ""),
        database=os.environ.get("DB_NAME", "coop_db"),
        charset="utf8",
    )


def get_temp_dir() -> Path:
    temp_dir = Path(tempfile.gettempdir()) / "api_temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir


async def save_upload(upload: Optional[UploadFile], prefix: str) -> Optional[Path]:
    if not upload or not upload.filename:
        return None
    if Path(upload.filename).suffix.lower() != ".pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    upload_dir = get_temp_dir()
    target = upload_dir / f"{prefix}_{os.urandom(8).hex()}.pdf"
    target.write_bytes(await upload.read())
    return target


def download_signed_pdf(url: Optional[str], prefix: str) -> Optional[Path]:
    """Download only a short-lived signed URL issued by this Supabase project."""
    if not url:
        return None
    expected_prefix = SUPABASE_URL + "/storage/v1/object/sign/"
    if not SUPABASE_URL or not url.startswith(expected_prefix):
        raise HTTPException(status_code=400, detail="Invalid file URL")
    response = httpx.get(url, follow_redirects=False, timeout=60)
    if response.status_code != 200 or len(response.content) > 20 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Unable to download the uploaded PDF")
    upload_dir = get_temp_dir()
    target = upload_dir / f"{prefix}_{os.urandom(8).hex()}.pdf"
    target.write_bytes(response.content)
    return target


def read_pdf(path: Optional[Path]) -> str:
    """Extract up to three CV/portfolio pages with Typhoon OCR or pypdf fallback."""
    if not path or not path.exists():
        return ""
    pages = []
    if ocr_document is not None:
        for page_num in range(1, 4):
            try:
                ocr_text = ocr_document(pdf_or_image_path=str(path), page_num=page_num)
                if ocr_text and ocr_text.strip():
                    pages.append(ocr_text)
            except Exception:
                break

    if pages:
        return "\n\n".join(pages)

    # Fallback to pypdf text extraction if Typhoon OCR / Poppler is not available
    try:
        import pypdf
        reader = pypdf.PdfReader(str(path))
        for page in reader.pages[:3]:
            extracted = page.extract_text()
            if extracted:
                pages.append(extracted)
        return "\n\n".join(pages)
    except Exception:
        return ""


def json_from_model(system: str, user: str, max_tokens: int) -> dict:
    api_key = os.environ.get("TYPHOON_API_KEY", "")
    if not api_key:
        raise HTTPException(status_code=500, detail="TYPHOON_API_KEY is not configured")
    try:
        current_client = OpenAI(api_key=api_key, base_url="https://api.opentyphoon.ai/v1")
        response = current_client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            temperature=0.2,
            max_tokens=max_tokens,
        )
        content = response.choices[0].message.content or ""
        content = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", content).strip()
        result = json.loads(content)
        if not isinstance(result, dict):
            raise ValueError("AI model did not return a JSON object")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Typhoon API error: {str(e)}") from e


@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL}


@app.post("/match")
async def match(
    profile: str = Form(...),
    cv: Optional[UploadFile] = File(None),
    portfolio: Optional[UploadFile] = File(None),
    cv_url: Optional[str] = Form(None),
    portfolio_url: Optional[str] = Form(None),
    authorization: Optional[str] = Header(None),
):
    verify_token(authorization)
    cv_path = await save_upload(cv, "cv") or download_signed_pdf(cv_url, "cv")
    portfolio_path = await save_upload(portfolio, "portfolio") or download_signed_pdf(portfolio_url, "portfolio")
    try:
        conn = db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, `ชื่อสถานประกอบการ` AS name, position, skills_required, interest_required, work_mode FROM companies")
        companies = cursor.fetchall()
        cursor.close()
        conn.close()
        if not companies:
            raise HTTPException(status_code=404, detail="No companies found")

        company_list = [{
            "company_id": c["id"], "company_name": c["name"],
            "position": c.get("position") or "", "skills_required": c.get("skills_required") or "",
            "interest_required": c.get("interest_required") or "", "work_mode": c.get("work_mode") or "",
        } for c in companies]
        document_text = f"CV:\n{read_pdf(cv_path)}\n\nPortfolio:\n{read_pdf(portfolio_path)}"
        system = """You are a careful Thai cooperative-education job matching analyst.
Return only valid JSON. Never invent company facts, qualifications, projects, or skills.
Scores express relevance of the supplied profile to the listed internship, not a hiring guarantee."""
        user = f"""Rank exactly the six most suitable companies from the provided company list.
Student profile:\n{profile}\n\nExtracted document text:\n{document_text[:30000]}
\nCompany list:\n{json.dumps(company_list, ensure_ascii=False)}

Return exactly:
{{"matches":[{{"company_id":123,"company_name":"name copied exactly from company list","match_score":0,"chance_score":0,"reason":"เหตุผลภาษาไทยสั้น ๆ อ้างอิงเฉพาะข้อมูลที่ให้"}}]}}
Use integer scores 0-100. company_id and company_name must come from the provided list."""
        result = json_from_model(system, user, max_tokens=1800)
        matches = result.get("matches")
        companies_by_id = {c["id"]: c for c in companies}
        if (
            not isinstance(matches, list)
            or len(matches) != 6
            or len({m.get("company_id") for m in matches}) != 6
            or any(m.get("company_id") not in companies_by_id for m in matches)
        ):
            raise ValueError("Typhoon returned invalid match records")
        # Keep database names authoritative, even if the model changes their spelling.
        cleaned = []
        for item in matches:
            company = companies_by_id[item["company_id"]]
            cleaned.append({
                "company_id": item["company_id"],
                "company_name": company["name"],
                "match_score": max(0, min(100, int(item.get("match_score", 0)))),
                "chance_score": max(0, min(100, int(item.get("chance_score", 0)))),
                "reason": str(item.get("reason", "")),
            })
        return {"matches": cleaned}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"AI matching failed: {exc}") from exc
    finally:
        for path in (cv_path, portfolio_path):
            if path and path.exists():
                path.unlink()


@app.post("/scan-cv")
async def scan_cv(cv: UploadFile = File(...), authorization: Optional[str] = Header(None)):
    verify_token(authorization)
    cv_path = await save_upload(cv, "scan")
    try:
        gemini_key = os.environ.get("GEMINI_API_KEY")
        if gemini_key and cv_path:
            try:
                import google.generativeai as genai
                genai.configure(api_key=gemini_key)
                myfile = genai.upload_file(str(cv_path))
                model = genai.GenerativeModel('models/gemini-1.5-flash')
                prompt = """Analyze this CV/Resume and extract information strictly in JSON format.
If a field is not found, leave it as an empty string.

Fields:
- full_name: Student name
- gpa: Grade point average (e.g., 3.50)
- department: Choose the closest between 'สาขาวิชาวิศวกรรมคอมพิวเตอร์' or 'สาขาวิชาเทคโนโลยีสารสนเทศ'
- major: Choose 'ซอฟต์แวร์' or 'เครือข่าย'
- interest: Main career interest (e.g., Frontend Developer)
- skill1: Top hard skill
- skill2: Second hard skill
- skill3: Soft skill
- work_format: Choose 'Hybrid', 'Onsite', or 'Remote'

Return ONLY valid JSON."""
                response = model.generate_content([prompt, myfile])
                text = response.text or ""
                text = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", text).strip()
                result = json.loads(text)
                if isinstance(result, dict):
                    return result
            except Exception:
                pass

        system = "Return only valid JSON. Extract facts only; use an empty string for absent fields."
        user = f"""Extract these fields from this CV OCR text:\n{read_pdf(cv_path)}
Return exactly {{"full_name":"","gpa":"","department":"","major":"","interest":"","skill1":"","skill2":"","skill3":"","work_format":""}}."""
        return json_from_model(system, user, max_tokens=500)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"CV scanning failed: {exc}") from exc
    finally:
        if cv_path and cv_path.exists():
            cv_path.unlink()
