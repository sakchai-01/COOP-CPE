import os
import re
import json
import warnings
import tempfile
from pathlib import Path
from typing import Optional, List, Dict, Any

warnings.filterwarnings("ignore")

from openai import OpenAI

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    from typhoon_ocr import ocr_document
except ImportError:
    ocr_document = None

TYPHOON_API_KEY = os.environ.get("TYPHOON_API_KEY", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL = os.environ.get("TYPHOON_MODEL", "typhoon-v2.5-30b-a3b-instruct")


def get_typhoon_client() -> Optional[OpenAI]:
    api_key = os.environ.get("TYPHOON_API_KEY", "")
    if not api_key:
        return None
    try:
        return OpenAI(api_key=api_key, base_url="https://api.opentyphoon.ai/v1")
    except Exception:
        return None


def read_pdf_bytes(pdf_bytes: bytes) -> str:
    if not pdf_bytes:
        return ""
    
    temp_dir = Path(tempfile.gettempdir())
    temp_path = temp_dir / f"temp_{os.urandom(8).hex()}.pdf"
    temp_path.write_bytes(pdf_bytes)
    
    pages = []
    if ocr_document is not None:
        for page_num in range(1, 4):
            try:
                ocr_text = ocr_document(pdf_or_image_path=str(temp_path), page_num=page_num)
                if ocr_text and ocr_text.strip():
                    pages.append(ocr_text)
            except Exception:
                break
                
    if pages:
        temp_path.unlink(missing_ok=True)
        return "\n\n".join(pages)

    try:
        import pypdf
        reader = pypdf.PdfReader(str(temp_path))
        for page in reader.pages[:3]:
            extracted = page.extract_text()
            if extracted:
                pages.append(extracted)
    except Exception:
        pass
        
    temp_path.unlink(missing_ok=True)
    return "\n\n".join(pages)


def scan_cv_pdf(cv_bytes: bytes) -> Dict[str, Any]:
    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    if gemini_key and genai is not None and cv_bytes:
        temp_path = Path(tempfile.gettempdir()) / f"scan_{os.urandom(8).hex()}.pdf"
        temp_path.write_bytes(cv_bytes)
        try:
            genai.configure(api_key=gemini_key)
            myfile = genai.upload_file(str(temp_path))
            model = genai.GenerativeModel('models/gemini-1.5-flash')
            prompt = """Analyze this CV/Resume and extract information strictly in JSON format.
Fields:
- full_name: Student name
- gpa: Grade point average (e.g., 3.50)
- department: Choose 'สาขาวิชาวิศวกรรมคอมพิวเตอร์' or 'สาขาวิชาเทคโนโลยีสารสนเทศ'
- major: Choose 'ซอฟต์แวร์', 'โรบอท', or 'ไซเบอร์'
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
            temp_path.unlink(missing_ok=True)
            if isinstance(result, dict):
                return result
        except Exception as e:
            print(f"Gemini scan error: {e}")
            temp_path.unlink(missing_ok=True)

    text_content = read_pdf_bytes(cv_bytes)
    client = get_typhoon_client()
    if client and text_content:
        system = "Return only valid JSON. Extract facts only; use an empty string for absent fields."
        user = f"""Extract these fields from this CV text:\n{text_content[:15000]}
Return exactly {{"full_name":"","gpa":"","department":"","major":"","interest":"","skill1":"","skill2":"","skill3":"","work_format":""}}."""
        try:
            res = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                temperature=0.2,
                max_tokens=500
            )
            raw = res.choices[0].message.content or ""
            raw = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", raw).strip()
            return json.loads(raw)
        except Exception as e:
            print(f"Typhoon scan error: {e}")

    return {
        "full_name": "", "gpa": "", "department": "สาขาวิชาวิศวกรรมคอมพิวเตอร์",
        "major": "ซอฟต์แวร์", "interest": "", "skill1": "", "skill2": "", "skill3": "", "work_format": "Hybrid"
    }


def match_companies_ai(student_profile: str, cv_bytes: bytes, portfolio_bytes: bytes, companies: List[Dict[str, Any]]) -> Dict[str, Any]:
    client = get_typhoon_client()
    doc_text = ""
    if cv_bytes:
        doc_text += f"CV Content:\n{read_pdf_bytes(cv_bytes)}\n\n"
    if portfolio_bytes:
        doc_text += f"Portfolio Content:\n{read_pdf_bytes(portfolio_bytes)}\n\n"

    company_list = [{
        "company_id": c["id"], "company_name": c["name"],
        "position": c.get("position") or "", "skills_required": c.get("skills_required") or "",
        "interest_required": c.get("interest_required") or "", "work_mode": c.get("work_mode") or "",
    } for c in companies]

    # Try LLM Match if Typhoon Client is configured
    if client:
        system = """You are a careful Thai cooperative-education job matching analyst.
Return only valid JSON. Never invent company facts, qualifications, projects, or skills.
Scores express relevance of the supplied profile to the listed internship, not a hiring guarantee."""
        user = f"""Rank exactly the four most suitable companies from the provided company list.
Student profile:\n{student_profile}\n\nExtracted document text:\n{doc_text[:20000]}
\nCompany list:\n{json.dumps(company_list, ensure_ascii=False)}

Return exactly:
{{"matches":[{{"company_id":123,"company_name":"name copied exactly from company list","match_score":0,"chance_score":0,"reason":"เหตุผลภาษาไทยสั้น ๆ อ้างอิงเฉพาะข้อมูลที่ให้"}}]}}
Use integer scores 0-100. company_id and company_name must come from the provided list."""
        try:
            res = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                temperature=0.2,
                max_tokens=1800
            )
            raw = res.choices[0].message.content or ""
            raw = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", raw).strip()
            parsed = json.loads(raw)
            matches = parsed.get("matches")
            if isinstance(matches, list) and len(matches) > 0:
                parsed["matches"] = matches[:4]
                return parsed
        except Exception as e:
            print(f"AI Match LLM error: {e}")

    # =========================================================================
    # DYNAMIC DEDICATED MATCHING ENGINE
    # Evaluates student profile vs ALL 23 companies and computes real scores
    # =========================================================================
    profile_lower = (student_profile + " " + doc_text).lower()
    
    # Extract GPA for scoring
    gpa_match = re.search(r"gpa:\s*([\d\.]+)", profile_lower)
    try:
        gpa = float(gpa_match.group(1)) if gpa_match else 3.0
    except ValueError:
        gpa = 3.0

    scored_companies = []
    
    for c in companies:
        c_name = c.get("name", "")
        c_pos = c.get("position", "") or ""
        c_skills = c.get("skills_required", "") or ""
        c_interest = c.get("interest_required", "") or ""
        c_major = c.get("major_required", "") or ""
        c_qual = c.get("qualifications", "") or ""
        c_workmode = c.get("work_mode", "") or ""
        
        c_text = f"{c_pos} {c_skills} {c_interest} {c_major} {c_qual} {c_workmode}".lower()
        
        score = 55.0  # Base score
        matched_tokens = []
        
        # Token match keywords
        keywords = re.findall(r"[\w\+\#\.]+", profile_lower)
        significant_kw = set(k for k in keywords if len(k) > 2 and k not in [
            'name', 'major', 'gpa', 'skills', 'interests', 'mode', 'student', 'สาขาวิชา', 'วิศวกรรม'
        ])
        
        for kw in significant_kw:
            if kw in c_text:
                score += 7.5
                if len(matched_tokens) < 3:
                    matched_tokens.append(kw)
        
        # Major check
        if ("software" in profile_lower or "ซอฟต์แวร์" in profile_lower) and ("software" in c_text or "programmer" in c_text or "web" in c_text):
            score += 12
        elif ("robot" in profile_lower or "โรบอท" in profile_lower) and ("robot" in c_text or "plc" in c_text or "automation" in c_text or "3d" in c_text):
            score += 12
        elif ("cyber" in profile_lower or "ไซเบอร์" in profile_lower) and ("cyber" in c_text or "security" in c_text or "network" in c_text):
            score += 12

        # GPA boost
        gpa_boost = min(10.0, max(0.0, (gpa - 2.0) * 5.0))
        score += gpa_boost

        # Cap score 65 - 98
        final_match_score = int(min(98, max(65, round(score))))
        
        # Chance score based on GPA and match score
        chance_base = 60 + (gpa - 2.0) * 15
        final_chance_score = int(min(96, max(60, round(chance_base + (final_match_score - 70) * 0.3))))
        
        # Build custom Thai reasoning
        pos_clean = c_pos.split("/")[0].strip() if c_pos else "ตำแหน่งที่เปิดรับ"
        if matched_tokens:
            kw_str = ", ".join(matched_tokens[:2])
            reason = f"ทักษะและความสนใจด้าน {kw_str} ตรงกับตำแหน่ง {pos_clean} ของ {c_name} (เกรดเฉลี่ย {gpa:.2f})"
        else:
            reason = f"คุณสมบัติเบื้องต้นและสาขาการศึกษาสอดคล้องกับ {pos_clean} ของ {c_name}"
            
        scored_companies.append({
            "company_id": c["id"],
            "company_name": c_name,
            "match_score": final_match_score,
            "chance_score": final_chance_score,
            "reason": reason
        })

    # Sort descending by match_score
    scored_companies.sort(key=lambda x: x["match_score"], reverse=True)
    
    # Return top 4 strictly
    return {"matches": scored_companies[:4]}
