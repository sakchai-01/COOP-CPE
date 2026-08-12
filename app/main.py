import os
import sys
import io
import warnings
from pathlib import Path
from typing import Optional, List

warnings.filterwarnings("ignore")

from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

# Adjust import paths
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.db import (
    verify_user, get_student_by_id, update_student_profile,
    get_all_companies, get_student_documents, save_student_document,
    get_all_documents, update_document_status, save_match_result,
    save_all_match_results, get_all_match_results,
    get_all_students, get_doc_stats, get_pending_students_with_docs,
    get_students_with_docs, get_student_docs_by_id,
    submit_student_application, bulk_update_docs_status
)
from app.storage import upload_document, get_signed_url
from app.ai_engine import scan_cv_pdf, match_companies_ai

app = FastAPI(title="Coop Education AI System")

# Session & CORS Middleware
SECRET_KEY = os.environ.get("SESSION_SECRET", "coop-super-secret-key-2026")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup Templates
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Serve root-level static files (PDFs, images)
app.mount("/static", StaticFiles(directory=str(BASE_DIR)), name="static_root")

# Helper for current user from session
def get_current_user(request: Request) -> Optional[dict]:
    return request.session.get("user")


# =========================================================
# Public Pages & Auth Routes
# =========================================================

@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    user = get_current_user(request)
    return templates.TemplateResponse("index.html", {"request": request, "user": user})


@app.get("/coop_info.php", response_class=HTMLResponse)
async def coop_info_page(request: Request):
    user = get_current_user(request)
    return templates.TemplateResponse("coop_info.html", {"request": request, "user": user})


@app.get("/download.php", response_class=HTMLResponse)
async def download_page(request: Request):
    user = get_current_user(request)
    return templates.TemplateResponse("download.html", {"request": request, "user": user})


@app.get("/contact.php", response_class=HTMLResponse)
async def contact_page(request: Request):
    user = get_current_user(request)
    return templates.TemplateResponse("contact.html", {"request": request, "user": user})


@app.get("/calendar.php", response_class=HTMLResponse)
async def calendar_page(request: Request):
    import csv, io
    user = get_current_user(request)
    cal_items = []
    cal_path = BASE_DIR / "calendar.csv"
    if cal_path.exists():
        try:
            text = cal_path.read_text(encoding="utf-8-sig")
            reader = csv.reader(io.StringIO(text))
            rows = list(reader)
            # Skip header rows (first 6 are titles/column headers)
            for row in rows[6:]:
                if len(row) >= 2 and row[0].strip().isdigit():
                    cal_items.append({
                        "num": row[0].strip(),
                        "activity": row[1].strip(),
                        "duration_4": row[2].strip() if len(row) > 2 else "",
                        "duration_6": row[3].strip() if len(row) > 3 else "",
                        "responsible": row[4].strip() if len(row) > 4 else "",
                        "note": row[5].strip() if len(row) > 5 else "",
                    })
        except Exception as e:
            print(f"Calendar CSV error: {e}")
    return templates.TemplateResponse("calendar.html", {"request": request, "user": user, "calendar_items": cal_items})




@app.get("/login", response_class=HTMLResponse)
@app.get("/login.html", response_class=HTMLResponse)
async def login_page(request: Request, error: Optional[str] = None):
    return templates.TemplateResponse("login.html", {"request": request, "error": error})


@app.post("/login")
@app.post("/login_process.php")
async def login_process(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    role: str = Form(...)
):
    user = verify_user(username.strip(), password.strip(), role.strip())
    if not user:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "ชื่อผู้ใช้ รหัสผ่าน หรือประเภทสิทธิ์ไม่ถูกต้อง"
        })
    
    # Set session
    request.session["user"] = user
    
    if user["role"] == "student":
        return RedirectResponse(url="/student_dashboard.php", status_code=303)
    elif user["role"] == "teacher":
        return RedirectResponse(url="/teacher_dashboard.php", status_code=303)
    elif user["role"] == "admin":
        return RedirectResponse(url="/admin_dashboard.php", status_code=303)
    
    return RedirectResponse(url="/", status_code=303)


@app.get("/logout")
@app.get("/logout.php")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)


# =========================================================
# Student Routes
# =========================================================

@app.get("/student_dashboard.php", response_class=HTMLResponse)
@app.get("/student/dashboard", response_class=HTMLResponse)
async def student_dashboard(request: Request, match_success: Optional[str] = None, upload_success: Optional[str] = None):
    user = get_current_user(request)
    if not user or user.get("role") != "student":
        return RedirectResponse(url="/login", status_code=303)

    student = get_student_by_id(user["username"])
    docs = get_student_documents(user["username"])
    
    has_match = bool(student.get("matchcompany"))
    has_docs = len(docs) > 0
    all_pass = len(docs) > 0 and all(d.get("status") == "ผ่าน" for d in docs)
    
    current_step = 1
    if has_match: current_step = 2
    if has_docs: current_step = 3
    if all_pass: current_step = 4
    
    progress_pct = int(((current_step - 1) / 3) * 100)

    return templates.TemplateResponse("student_dashboard.html", {
        "request": request,
        "user": user,
        "student": student,
        "docs": docs,
        "current_step": current_step,
        "progress_pct": progress_pct,
        "match_success": bool(match_success),
        "upload_success": bool(upload_success)
    })


@app.get("/ai_match_input.php", response_class=HTMLResponse)
async def ai_match_input_page(request: Request, msg: Optional[str] = None):
    user = get_current_user(request)
    if not user or user.get("role") != "student":
        return RedirectResponse(url="/login", status_code=303)

    student = get_student_by_id(user["username"])
    companies = get_all_companies()
    return templates.TemplateResponse("ai_match_input.html", {
        "request": request,
        "user": user,
        "student": student,
        "msg": msg,
        "company_count": len(companies)
    })


@app.post("/api/student/match")
@app.post("/ai_match_process.php")
async def process_ai_match(
    request: Request,
    student_id: str = Form(...),
    full_name: str = Form(...),
    department: str = Form("สาขาวิชาวิศวกรรมคอมพิวเตอร์"),
    major: str = Form("ซอฟต์แวร์"),
    gpa: str = Form("3.50"),
    interest: str = Form(""),
    skill1: str = Form(""),
    skill2: str = Form(""),
    skill3: str = Form(""),
    work_format: str = Form("Hybrid"),
    cv: Optional[UploadFile] = File(None),
    portfolio: Optional[UploadFile] = File(None)
):
    import uuid, datetime
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    # GPA Check (< 2.00 Warning)
    try:
        gpa_val = float(gpa.strip())
    except Exception:
        gpa_val = 0.0

    if gpa_val < 2.00:
        return templates.TemplateResponse("ai_match_input.html", {
            "request": request,
            "user": user,
            "student": get_student_by_id(user["username"]),
            "msg": "เกรดเฉลี่ยต่ำกว่าเกณฑ์ ไม่อนุญาต ให้ออกฝึกสหกิจ โปรดติดต่ออาจารย์ที่ปรึกษาเพื่อสอบถามเพิ่มเติม",
            "is_warning": True,
            "company_count": len(get_all_companies())
        })

    # Read uploaded file bytes
    cv_bytes = await cv.read() if (cv and cv.filename) else b""
    port_bytes = await portfolio.read() if (portfolio and portfolio.filename) else b""

    # Save student profile updates
    skills_text = ", ".join([s for s in [skill1, skill2, skill3] if s])
    update_student_profile(student_id, {
        "fullname": full_name,
        "major": major,
        "gpa": gpa,
        "career_interest": interest,
        "skills": skills_text,
        "work_mode": work_format
    })

    # Run AI Match
    companies = get_all_companies()
    profile_text = f"Name: {full_name}, Major: {major}, GPA: {gpa}, Skills: {skills_text}, Interests: {interest}, Mode: {work_format}"
    ai_result = match_companies_ai(profile_text, cv_bytes, port_bytes, companies)

    matches = ai_result.get("matches", [])

    # Generate batch ID and save ALL matches to DB
    batch_id = f"{student_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    save_all_match_results(student_id, matches, batch_id)

    # Store in session so GET /ai_match_result.php can re-display without re-running AI
    request.session["last_matches"] = matches
    request.session["last_batch_id"] = batch_id

    return templates.TemplateResponse("ai_match_result.html", {
        "request": request,
        "user": user,
        "matches": matches
    })


@app.post("/scan-cv")
@app.post("/scan_cv_ajax.php")
@app.post("/api/student/scan-cv")
async def scan_cv_endpoint(cv: UploadFile = File(...), cv_file: Optional[UploadFile] = File(None)):
    target = cv or cv_file
    if not target:
        return JSONResponse({"error": "No file uploaded"}, status_code=400)
    
    content = await target.read()
    res = scan_cv_pdf(content)
    return JSONResponse(res)


@app.get("/ai_match_result.php", response_class=HTMLResponse)
async def ai_match_result_page(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    # Read from session (set by POST route after AI finishes)
    matches = request.session.get("last_matches", [])

    # If session is empty (direct URL visit), redirect back to input
    if not matches:
        return RedirectResponse(url="/ai_match_input.php", status_code=303)

    return templates.TemplateResponse("ai_match_result.html", {
        "request": request,
        "user": user,
        "matches": matches
    })


@app.get("/submit_docs.php", response_class=HTMLResponse)
async def submit_docs_page(request: Request, upload_success: Optional[str] = None):
    user = get_current_user(request)
    if not user or user.get("role") != "student":
        return RedirectResponse(url="/login", status_code=303)

    REQUIRED_DOCS = {
        "doc1": "เอกสาร COOP - PSRU02",
        "doc2": "ใบแสดงผลการศึกษา",
        "doc3": "ไฟล์ pdf (ตั้งชื่อไฟล์ : CV-Coop-ชื่อ สกุลภาษาอังกฤษ)",
        "doc4": "ไฟล์ pdf. เกียรติบัตร psru digital test",
        "doc5": "สำเนาบัตรประจำตัวประชาชน",
        "doc6": "สำเนาทะเบียนบ้าน",
        "doc7": "สำเนาบัตรประจำตัวนักศึกษา",
        "doc8": "ไฟล์ pdf. เกียรติบัตร psru english test",
    }

    all_docs = get_student_documents(user["username"])
    uploaded_docs = {d["doc_type"]: d for d in all_docs if "doc_type" in d}
    failed_count = sum(1 for d in all_docs if d.get("status") == "ไม่ผ่าน")
    uploaded_count = len(uploaded_docs)
    can_submit = (uploaded_count == 8 and failed_count == 0)

    return templates.TemplateResponse("submit_docs.html", {
        "request": request,
        "user": user,
        "required_docs": REQUIRED_DOCS,
        "uploaded_docs": uploaded_docs,
        "uploaded_count": uploaded_count,
        "can_submit": can_submit,
        "upload_success": bool(upload_success),
    })


@app.post("/upload_process.php")
@app.post("/upload_file.php")
async def upload_file_process(
    request: Request,
    doc_type: str = Form("doc1"),
    uploaded_file: UploadFile = File(...)
):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    content = await uploaded_file.read()
    ref_path = upload_document(content, "documents", uploaded_file.filename or "doc.pdf")
    # Save with doc_type
    from app.db import get_db_connection
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO documents (student_id, student_name, doc_type, file_name, status) VALUES (%s, %s, %s, %s, 'รอตรวจ') "
                "ON DUPLICATE KEY UPDATE file_name=%s, status='รอตรวจ'",
                (user["username"], user["username"], doc_type,
                 uploaded_file.filename or "doc.pdf", uploaded_file.filename or "doc.pdf")
            )
            conn.commit()
            cursor.close()
            conn.close()
        except Exception:
            if conn.is_connected(): conn.close()
    else:
        save_student_document(user["username"], ref_path)

    return RedirectResponse(url="/submit_docs.php?upload_success=1", status_code=303)


@app.post("/submit_app_process.php")
async def submit_app_process(request: Request):
    user = get_current_user(request)
    if not user or user.get("role") != "student":
        return RedirectResponse(url="/login", status_code=303)
    submit_student_application(user["username"])
    return RedirectResponse(url="/student_dashboard.php?match_success=1", status_code=303)


# =========================================================
# Teacher & Admin Routes
# =========================================================

@app.get("/teacher_dashboard.php", response_class=HTMLResponse)
@app.get("/teacher/dashboard", response_class=HTMLResponse)
async def teacher_dashboard(request: Request):
    user = get_current_user(request)
    if not user or user.get("role") not in ["teacher", "admin"]:
        return RedirectResponse(url="/login", status_code=303)

    stats = get_doc_stats()
    return templates.TemplateResponse("teacher_dashboard.html", {
        "request": request,
        "user": user,
        "stats": stats
    })


@app.get("/teacher_check_docs.php", response_class=HTMLResponse)
async def teacher_check_docs_page(request: Request):
    user = get_current_user(request)
    if not user or user.get("role") not in ["teacher", "admin"]:
        return RedirectResponse(url="/login", status_code=303)

    pending_students = get_pending_students_with_docs()
    return templates.TemplateResponse("teacher_check_docs.html", {
        "request": request,
        "user": user,
        "pending_students": pending_students
    })


@app.get("/teacher_check_std.php", response_class=HTMLResponse)
async def teacher_check_std_page(request: Request, id: Optional[str] = None):
    user = get_current_user(request)
    if not user or user.get("role") not in ["teacher", "admin"]:
        return RedirectResponse(url="/login", status_code=303)
    if not id:
        return RedirectResponse(url="/teacher_check_docs.php", status_code=303)

    DOC_LABELS = {
        "doc1": "เอกสาร COOP - PSRU02",
        "doc2": "ใบแสดงผลการศึกษา",
        "doc3": "CV-Coop",
        "doc4": "เกียรติบัตร psru digital test",
        "doc5": "สำเนาบัตรประจำตัวประชาชน",
        "doc6": "สำเนาทะเบียนบ้าน",
        "doc7": "สำเนาบัตรประจำตัวนักศึกษา",
        "doc8": "เกียรติบัตร psru english test",
    }
    student_info = get_student_by_id(id)
    docs = get_student_docs_by_id(id)
    return templates.TemplateResponse("teacher_check_std.html", {
        "request": request,
        "user": user,
        "student_id": id,
        "student_info": student_info,
        "docs": docs,
        "doc_labels": DOC_LABELS,
    })


@app.post("/api/teacher/update-doc-status")
@app.post("/update_doc_status.php")
async def update_doc_status_endpoint(
    request: Request,
    doc_id: int = Form(...),
    status: str = Form(...),
    comment: str = Form("")
):
    update_document_status(doc_id, status, comment)
    # Try to get the student_id for redirect
    referer = request.headers.get("referer", "/teacher_check_docs.php")
    return RedirectResponse(url=referer, status_code=303)


@app.post("/api/teacher/bulk-doc-status")
async def bulk_doc_status_endpoint(
    request: Request,
    student_id: str = Form(...),
    status: str = Form(...),
    comment: str = Form("")
):
    bulk_update_docs_status(student_id, status, comment)
    return RedirectResponse(url=f"/teacher_check_std.php?id={student_id}", status_code=303)


@app.get("/teacher_std_info.php", response_class=HTMLResponse)
async def teacher_std_info_page(request: Request, q: Optional[str] = None):
    user = get_current_user(request)
    if not user or user.get("role") not in ["teacher", "admin"]:
        return RedirectResponse(url="/login", status_code=303)

    students = get_all_students(search=q or "")
    return templates.TemplateResponse("teacher_std_info.html", {
        "request": request,
        "user": user,
        "students": students,
        "search": q or "",
    })


@app.get("/teacher_review_results.php", response_class=HTMLResponse)
async def teacher_review_results_page(request: Request, status: Optional[str] = None):
    user = get_current_user(request)
    if not user or user.get("role") not in ["teacher", "admin"]:
        return RedirectResponse(url="/login", status_code=303)

    page_titles = {
        "passed": "เอกสารที่ผ่าน",
        "failed": "เอกสารที่ไม่ผ่าน",
        "pending": "เอกสารรอตรวจ",
    }
    students = get_students_with_docs(status_filter=status or "")
    return templates.TemplateResponse("teacher_review_results.html", {
        "request": request,
        "user": user,
        "students": students,
        "status_filter": status or "",
        "page_title": page_titles.get(status or "", "เอกสารทั้งหมด"),
    })


@app.get("/api/teacher/export-excel")
@app.get("/export_excel.php")
async def export_excel_endpoint():
    try:
        import openpyxl
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Coop Students"
        ws.append(["ID", "Student Name", "Status", "Company Match"])
        
        results = get_all_match_results()
        for idx, r in enumerate(results, start=1):
            ws.append([idx, r.get("student_id", ""), "Approved", r.get("company_name", "")])
            
        stream = io.BytesIO()
        wb.save(stream)
        stream.seek(0)
        
        headers = {'Content-Disposition': 'attachment; filename="coop_students_export.xlsx"'}
        return StreamingResponse(stream, headers=headers, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        return JSONResponse({"error": f"Export failed: {str(e)}"}, status_code=500)


@app.get("/admin_dashboard.php", response_class=HTMLResponse)
@app.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    user = get_current_user(request)
    if not user or user.get("role") != "admin":
        return RedirectResponse(url="/login", status_code=303)

    stats = get_doc_stats()
    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request,
        "user": user,
        "stats": stats
    })


@app.get("/company_info.php", response_class=HTMLResponse)
async def company_info_page(request: Request):
    user = get_current_user(request)
    companies = get_all_companies()
    return templates.TemplateResponse("company_info.html", {
        "request": request,
        "user": user,
        "companies": companies
    })


@app.get("/health")
def health():
    return {"status": "ok", "service": "Coop FastAPI Application", "runtime": "Python"}


# Mount static files for workspace root (CSS, PNG, JPG, PDF)
app.mount("/", StaticFiles(directory=str(BASE_DIR), html=False), name="static")

if __name__ == "__main__":
    import uvicorn
    print("Starting Coop Education FastAPI Server on http://127.0.0.1:8000...")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
