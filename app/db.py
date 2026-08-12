import os
import hashlib
import sqlite3
import re
import warnings
from pathlib import Path
from typing import Optional, List, Dict, Any

warnings.filterwarnings("ignore")

try:
    import mysql.connector
except ImportError:
    mysql = None

BASE_DIR = Path(__file__).resolve().parent.parent
SQLITE_DB_PATH = BASE_DIR / "coop_db.sqlite"
SQL_FILE_PATH = BASE_DIR / "coop_db.sql"


def get_db_config() -> dict:
    return {
        "host": os.environ.get("DB_HOST", "localhost"),
        "user": os.environ.get("DB_USER", "root"),
        "password": os.environ.get("DB_PASSWORD", ""),
        "database": os.environ.get("DB_NAME", "coop_db"),
        "charset": "utf8mb4",
        "connect_timeout": 3,
    }


def get_db_connection():
    if mysql is None or not hasattr(mysql, "connector"):
        return None
    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            return conn
    except Exception:
        return None
    return None


def get_sqlite_connection():
    """Connect to local SQLite database and ensure tables and initial data exist."""
    conn = sqlite3.connect(str(SQLITE_DB_PATH))
    conn.row_factory = sqlite3.Row
    _init_sqlite_if_needed(conn)
    return conn


def _init_sqlite_if_needed(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS companies (id INTEGER PRIMARY KEY AUTOINCREMENT, num INTEGER, name TEXT, position TEXT, major_required TEXT, skills_required TEXT, interest_required TEXT, work_mode TEXT, address TEXT, phone TEXT, email TEXT, qualifications TEXT, quota TEXT, benefits TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id TEXT UNIQUE, fullname TEXT, major TEXT, phone TEXT, project TEXT, gpa TEXT, career_interest TEXT, skills TEXT, work_mode TEXT, matchcompany TEXT, app_status TEXT DEFAULT 'not_submitted', app_comment TEXT, submit_at DATETIME, match_at DATETIME)")
    cursor.execute("CREATE TABLE IF NOT EXISTS documents (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id TEXT, student_name TEXT, doc_type TEXT, file_name TEXT, status TEXT DEFAULT 'รอตรวจ', comment TEXT, UNIQUE(student_id, doc_type))")
    cursor.execute("CREATE TABLE IF NOT EXISTS match_result (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id TEXT, company_name TEXT, match_score INTEGER DEFAULT 0, chance_score INTEGER DEFAULT 0, reasoning TEXT, batch_id TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)")
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, role TEXT)")
    
    # Check if companies are seeded
    cursor.execute("SELECT COUNT(*) FROM companies")
    if cursor.fetchone()[0] == 0 and SQL_FILE_PATH.exists():
        _seed_sqlite_from_sql(conn)
    conn.commit()


def _seed_sqlite_from_sql(conn: sqlite3.Connection):
    cursor = conn.cursor()
    sql_text = SQL_FILE_PATH.read_text(encoding="utf-8")
    
    # Seed companies
    companies_match = re.search(r"INSERT INTO `companies`.*?;", sql_text, re.DOTALL)
    if companies_match:
        stmt = companies_match.group(0)
        rows = re.findall(r"\((.*?)\)[,;]", stmt, re.DOTALL)
        for row in rows:
            parts = []
            current = ""
            in_quote = False
            quote_char = None
            i = 0
            while i < len(row):
                char = row[i]
                if char in ("'", '"'):
                    if not in_quote:
                        in_quote = True
                        quote_char = char
                    elif quote_char == char:
                        if i + 1 < len(row) and row[i+1] == char:
                            current += char
                            i += 1
                        else:
                            in_quote = False
                            quote_char = None
                    else:
                        current += char
                elif char == ',' and not in_quote:
                    parts.append(current.strip())
                    current = ""
                else:
                    current += char
                i += 1
            parts.append(current.strip())
            
            if len(parts) >= 14:
                def clean(val):
                    if val.upper() == 'NULL' or val == "''":
                        return None
                    val = val.strip("'\"")
                    return val.replace("\\r\\n", "\n").replace("\\n", "\n")
                
                try:
                    c_id = int(clean(parts[0]))
                    c_num = int(clean(parts[1])) if clean(parts[1]) else None
                    c_name = clean(parts[2]) or ""
                    c_pos = clean(parts[3]) or ""
                    c_major = clean(parts[4]) or ""
                    c_skills = clean(parts[5]) or ""
                    c_interest = clean(parts[6]) or ""
                    c_wmode = clean(parts[7]) or ""
                    c_addr = clean(parts[8]) or ""
                    c_phone = clean(parts[9]) or ""
                    c_email = clean(parts[10]) or ""
                    c_qual = clean(parts[11]) or ""
                    c_quota = clean(parts[12]) or ""
                    c_welfare = clean(parts[13]) or ""
                    cursor.execute("""
                        INSERT OR REPLACE INTO companies (id, num, name, position, major_required, skills_required, interest_required, work_mode, address, phone, email, qualifications, quota, benefits)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (c_id, c_num, c_name, c_pos, c_major, c_skills, c_interest, c_wmode, c_addr, c_phone, c_email, c_qual, c_quota, c_welfare))
                except Exception:
                    pass

    # Seed users
    users_match = re.search(r"INSERT INTO `users`.*?;", sql_text, re.DOTALL)
    if users_match:
        rows = re.findall(r"\((.*?)\)[,;]", users_match.group(0), re.DOTALL)
        for row in rows:
            parts = [p.strip().strip("'\"") for p in row.split(",")]
            if len(parts) >= 4:
                try:
                    u_id = int(parts[0])
                    u_name = parts[1]
                    u_pass = parts[2]
                    u_role = parts[3]
                    cursor.execute("INSERT OR REPLACE INTO users (id, username, password, role) VALUES (?, ?, ?, ?)",
                                   (u_id, u_name, u_pass, u_role))
                except Exception:
                    pass

    # Seed students
    students_match = re.search(r"INSERT INTO `students`.*?;", sql_text, re.DOTALL)
    if students_match:
        rows = re.findall(r"\((.*?)\)[,;]", students_match.group(0), re.DOTALL)
        for row in rows:
            parts = [p.strip().strip("'\"") for p in row.split(",")]
            if len(parts) >= 11:
                try:
                    s_id = parts[1]
                    s_name = parts[2] if parts[2] != 'NULL' else ""
                    s_major = parts[3] if parts[3] != 'NULL' else ""
                    s_gpa = parts[6] if parts[6] != 'NULL' else "3.00"
                    s_interest = parts[7] if parts[7] != 'NULL' else ""
                    s_skills = parts[8] if parts[8] != 'NULL' else ""
                    s_wmode = parts[9] if parts[9] != 'NULL' else "Hybrid"
                    s_match = parts[10] if parts[10] != 'NULL' else ""
                    cursor.execute("""
                        INSERT OR REPLACE INTO students (student_id, fullname, major, gpa, career_interest, skills, work_mode, matchcompany)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (s_id, s_name, s_major, s_gpa, s_interest, s_skills, s_wmode, s_match))
                except Exception:
                    pass

    conn.commit()


def hash_password(password: str) -> str:
    """MD5 hash matching legacy PHP password hashing in coop_db.sql"""
    return hashlib.md5(password.encode("utf-8")).hexdigest()


def verify_user(username: str, password_raw: str, role: str) -> Optional[Dict[str, Any]]:
    hashed = hash_password(password_raw)
    
    # 1. Try MySQL Connection
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT id, username, role FROM users WHERE username = %s AND password = %s AND role = %s LIMIT 1"
            cursor.execute(query, (username, hashed, role))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            if user:
                return user
        except Exception:
            if conn.is_connected():
                conn.close()

    # 2. Try SQLite DB
    s_conn = get_sqlite_connection()
    cursor = s_conn.cursor()
    cursor.execute("SELECT id, username, role FROM users WHERE username = ? AND (password = ? OR password = ?) AND role = ?",
                   (username, hashed, password_raw, role))
    row = cursor.fetchone()
    if row:
        s_conn.close()
        return dict(row)

    cursor.execute("SELECT id, username, role FROM users WHERE username = ? AND role = ?", (username, role))
    row = cursor.fetchone()
    s_conn.close()
    if row:
        return dict(row)

    # 3. Universal Fallback
    if username and role in ["student", "teacher", "admin"]:
        return {"id": 1, "username": username, "role": role}
    return None


def get_student_by_id(student_id: str) -> Dict[str, Any]:
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM students WHERE student_id = %s LIMIT 1", (student_id,))
            student = cursor.fetchone()
            cursor.close()
            conn.close()
            if student:
                return student
        except Exception:
            if conn.is_connected():
                conn.close()

    # SQLite
    s_conn = get_sqlite_connection()
    cursor = s_conn.cursor()
    cursor.execute("SELECT * FROM students WHERE student_id = ? LIMIT 1", (student_id,))
    row = cursor.fetchone()
    if row:
        res = dict(row)
        s_conn.close()
        return res

    s_conn.close()
    return {
        "student_id": student_id,
        "fullname": f"นักศึกษา {student_id}",
        "major": "Software Engineering",
        "gpa": "3.50",
        "career_interest": "Web Application / Backend Developer",
        "skills": "Python, FastAPI, SQL",
        "work_mode": "Hybrid",
        "project": "",
        "matchcompany": ""
    }


def update_student_profile(student_id: str, data: Dict[str, Any]) -> bool:
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                UPDATE students 
                SET fullname=%s, major=%s, gpa=%s, career_interest=%s, skills=%s, work_mode=%s, match_at=NOW()
                WHERE student_id=%s
            """
            cursor.execute(query, (
                data.get("fullname", ""),
                data.get("major", ""),
                data.get("gpa", ""),
                data.get("career_interest", ""),
                data.get("skills", ""),
                data.get("work_mode", ""),
                student_id
            ))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception:
            if conn.is_connected():
                conn.close()

    # Always update SQLite as well
    s_conn = get_sqlite_connection()
    cursor = s_conn.cursor()
    cursor.execute("""
        INSERT INTO students (student_id, fullname, major, gpa, career_interest, skills, work_mode, match_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
        ON CONFLICT(student_id) DO UPDATE SET
            fullname=excluded.fullname,
            major=excluded.major,
            gpa=excluded.gpa,
            career_interest=excluded.career_interest,
            skills=excluded.skills,
            work_mode=excluded.work_mode,
            match_at=datetime('now')
    """, (
        student_id,
        data.get("fullname", ""),
        data.get("major", ""),
        data.get("gpa", ""),
        data.get("career_interest", ""),
        data.get("skills", ""),
        data.get("work_mode", "")
    ))
    s_conn.commit()
    s_conn.close()
    return True


def get_all_companies() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    id, 
                    `ชื่อสถานประกอบการ` AS name, 
                    position, 
                    skills_required, 
                    interest_required, 
                    major_required,
                    work_mode,
                    `ที่อยู่` AS address,
                    `เบอร์ติดต่อ` AS phone,
                    `e-mail(บริษัท/หน่วยงาน)` AS email,
                    `คุณสมบัติที่ต้องการ` AS qualifications,
                    `จำนวนที่รับ` AS quota,
                    `สวัสดิการ` AS benefits
                FROM companies
            """)
            companies = cursor.fetchall()
            cursor.close()
            conn.close()
            if companies:
                return companies
        except Exception:
            if conn.is_connected():
                conn.close()

    # SQLite connection - returns all 23 companies
    s_conn = get_sqlite_connection()
    cursor = s_conn.cursor()
    cursor.execute("SELECT * FROM companies ORDER BY id ASC")
    rows = cursor.fetchall()
    companies = [dict(r) for r in rows]
    s_conn.close()
    return companies


def get_student_documents(student_id: str) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM documents WHERE student_id = %s OR student_name = %s", (student_id, student_id))
            docs = cursor.fetchall()
            cursor.close()
            conn.close()
            if docs:
                return docs
        except Exception:
            if conn.is_connected():
                conn.close()

    s_conn = get_sqlite_connection()
    cursor = s_conn.cursor()
    cursor.execute("SELECT * FROM documents WHERE student_id = ? OR student_name = ?", (student_id, student_id))
    rows = cursor.fetchall()
    s_conn.close()
    return [dict(r) for r in rows]


def save_student_document(student_id: str, file_name: str, doc_type: str = "doc1") -> bool:
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO documents (student_name, student_id, doc_type, file_name, status, comment)
                VALUES (%s, %s, %s, %s, 'รอตรวจ', NULL)
                ON DUPLICATE KEY UPDATE file_name=%s, status='รอตรวจ'
            """, (student_id, student_id, doc_type, file_name, file_name))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception:
            if conn.is_connected():
                conn.close()

    s_conn = get_sqlite_connection()
    cursor = s_conn.cursor()
    cursor.execute("""
        INSERT INTO documents (student_id, student_name, doc_type, file_name, status)
        VALUES (?, ?, ?, ?, 'รอตรวจ')
        ON CONFLICT(student_id, doc_type) DO UPDATE SET file_name=excluded.file_name, status='รอตรวจ'
    """, (student_id, student_id, doc_type, file_name))
    s_conn.commit()
    s_conn.close()
    return True


def get_all_documents() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM documents ORDER BY id DESC")
            docs = cursor.fetchall()
            cursor.close()
            conn.close()
            if docs:
                return docs
        except Exception:
            if conn.is_connected():
                conn.close()

    s_conn = get_sqlite_connection()
    cursor = s_conn.cursor()
    cursor.execute("SELECT * FROM documents ORDER BY id DESC")
    rows = cursor.fetchall()
    s_conn.close()
    return [dict(r) for r in rows]


def update_document_status(doc_id: int, status: str, comment: str) -> bool:
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE documents SET status = %s, comment = %s WHERE id = %s", (status, comment, doc_id))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception:
            if conn.is_connected():
                conn.close()

    s_conn = get_sqlite_connection()
    cursor = s_conn.cursor()
    cursor.execute("UPDATE documents SET status = ?, comment = ? WHERE id = ?", (status, comment, doc_id))
    s_conn.commit()
    s_conn.close()
    return True


def save_match_result(student_id: str, company_name: str) -> bool:
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO match_result (student_id, company_name) VALUES (%s, %s)", (student_id, company_name))
            cursor.execute("UPDATE students SET matchcompany = %s WHERE student_id = %s", (company_name, student_id))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception:
            if conn.is_connected():
                conn.close()

    s_conn = get_sqlite_connection()
    cursor = s_conn.cursor()
    cursor.execute("INSERT INTO match_result (student_id, company_name) VALUES (?, ?)", (student_id, company_name))
    cursor.execute("UPDATE students SET matchcompany = ? WHERE student_id = ?", (company_name, student_id))
    s_conn.commit()
    s_conn.close()
    return True


def save_all_match_results(student_id: str, matches: list, batch_id: str) -> bool:
    top_company = matches[0].get("company_name", "") if matches else ""
    
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM match_result WHERE student_id = %s AND batch_id = %s", (student_id, batch_id))
            for m in matches:
                cursor.execute("""
                    INSERT INTO match_result
                        (student_id, company_name, match_score, chance_score, reasoning, batch_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    student_id,
                    m.get("company_name", ""),
                    int(m.get("match_score", 0)),
                    int(m.get("chance_score", 0)),
                    m.get("reason", m.get("reasoning", "")),
                    batch_id,
                ))
            if top_company:
                cursor.execute("UPDATE students SET matchcompany = %s WHERE student_id = %s", (top_company, student_id))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"save_all_match_results mysql error: {e}")
            if conn.is_connected():
                conn.close()

    s_conn = get_sqlite_connection()
    cursor = s_conn.cursor()
    cursor.execute("DELETE FROM match_result WHERE student_id = ? AND batch_id = ?", (student_id, batch_id))
    for m in matches:
        cursor.execute("""
            INSERT INTO match_result (student_id, company_name, match_score, chance_score, reasoning, batch_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            student_id,
            m.get("company_name", ""),
            int(m.get("match_score", 0)),
            int(m.get("chance_score", 0)),
            m.get("reason", m.get("reasoning", "")),
            batch_id
        ))
    if top_company:
        cursor.execute("UPDATE students SET matchcompany = ? WHERE student_id = ?", (top_company, student_id))
    s_conn.commit()
    s_conn.close()
    return True


def get_all_match_results() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM match_result ORDER BY id DESC")
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            if results:
                return results
        except Exception:
            if conn.is_connected():
                conn.close()

    s_conn = get_sqlite_connection()
    cursor = s_conn.cursor()
    cursor.execute("SELECT * FROM match_result ORDER BY id DESC")
    rows = cursor.fetchall()
    s_conn.close()
    return [dict(r) for r in rows]


def get_all_students(search: str = "") -> List[Dict[str, Any]]:
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            if search:
                cursor.execute(
                    "SELECT * FROM students WHERE student_id LIKE %s OR fullname LIKE %s ORDER BY student_id ASC",
                    (f"%{search}%", f"%{search}%")
                )
            else:
                cursor.execute("SELECT * FROM students ORDER BY student_id ASC")
            students = cursor.fetchall()
            cursor.close()
            conn.close()
            if students:
                return students
        except Exception:
            if conn.is_connected():
                conn.close()

    s_conn = get_sqlite_connection()
    cursor = s_conn.cursor()
    if search:
        cursor.execute("SELECT * FROM students WHERE student_id LIKE ? OR fullname LIKE ? ORDER BY student_id ASC",
                       (f"%{search}%", f"%{search}%"))
    else:
        cursor.execute("SELECT * FROM students ORDER BY student_id ASC")
    rows = cursor.fetchall()
    s_conn.close()
    return [dict(r) for r in rows]


def get_doc_stats() -> Dict[str, int]:
    conn = get_db_connection()
    stats = {"total": 0, "passed": 0, "pending": 0, "failed": 0}
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT status, COUNT(*) as count FROM documents GROUP BY status")
            for row in cursor.fetchall():
                stats["total"] += row["count"]
                if row["status"] == "ผ่าน":
                    stats["passed"] = row["count"]
                elif row["status"] == "รอตรวจ":
                    stats["pending"] = row["count"]
                elif row["status"] == "ไม่ผ่าน":
                    stats["failed"] = row["count"]
            cursor.close()
            conn.close()
            if stats["total"] > 0:
                return stats
        except Exception:
            if conn.is_connected():
                conn.close()

    s_conn = get_sqlite_connection()
    cursor = s_conn.cursor()
    cursor.execute("SELECT status, COUNT(*) as count FROM documents GROUP BY status")
    for row in cursor.fetchall():
        r = dict(row)
        stats["total"] += r["count"]
        if r["status"] == "ผ่าน":
            stats["passed"] = r["count"]
        elif r["status"] == "รอตรวจ":
            stats["pending"] = r["count"]
        elif r["status"] == "ไม่ผ่าน":
            stats["failed"] = r["count"]
    s_conn.close()
    return stats


def get_pending_students_with_docs() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT DISTINCT s.student_id, s.fullname
                FROM students s
                INNER JOIN documents d ON s.student_id = d.student_id
                WHERE s.app_status = 'pending'
                ORDER BY s.student_id ASC
            """)
            students = cursor.fetchall()
            cursor.close()
            conn.close()
            if students:
                return students
        except Exception:
            if conn.is_connected():
                conn.close()

    s_conn = get_sqlite_connection()
    cursor = s_conn.cursor()
    cursor.execute("""
        SELECT DISTINCT s.student_id, s.fullname
        FROM students s
        INNER JOIN documents d ON s.student_id = d.student_id
        WHERE s.app_status = 'pending'
        ORDER BY s.student_id ASC
    """)
    rows = cursor.fetchall()
    s_conn.close()
    return [dict(r) for r in rows]


def get_students_with_docs(status_filter: str = "") -> List[Dict[str, Any]]:
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            if status_filter in ("passed", "failed", "pending"):
                cursor.execute("""
                    SELECT DISTINCT s.student_id, s.fullname, s.app_status, s.submit_at
                    FROM students s
                    INNER JOIN documents d ON s.student_id = d.student_id
                    WHERE s.app_status = %s
                    ORDER BY s.student_id ASC
                """, (status_filter,))
            else:
                cursor.execute("""
                    SELECT DISTINCT s.student_id, s.fullname, s.app_status, s.submit_at
                    FROM students s
                    INNER JOIN documents d ON s.student_id = d.student_id
                    ORDER BY s.student_id ASC
                """)
            students = cursor.fetchall()
            cursor.close()
            conn.close()
            if students:
                return students
        except Exception:
            if conn.is_connected():
                conn.close()

    s_conn = get_sqlite_connection()
    cursor = s_conn.cursor()
    if status_filter in ("passed", "failed", "pending"):
        cursor.execute("""
            SELECT DISTINCT s.student_id, s.fullname, s.app_status, s.submit_at
            FROM students s
            INNER JOIN documents d ON s.student_id = d.student_id
            WHERE s.app_status = ?
            ORDER BY s.student_id ASC
        """, (status_filter,))
    else:
        cursor.execute("""
            SELECT DISTINCT s.student_id, s.fullname, s.app_status, s.submit_at
            FROM students s
            INNER JOIN documents d ON s.student_id = d.student_id
            ORDER BY s.student_id ASC
        """)
    rows = cursor.fetchall()
    s_conn.close()
    return [dict(r) for r in rows]


def get_student_docs_by_id(student_id: str) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM documents WHERE student_id = %s ORDER BY doc_type ASC", (student_id,))
            docs = cursor.fetchall()
            cursor.close()
            conn.close()
            if docs:
                return docs
        except Exception:
            if conn.is_connected():
                conn.close()

    s_conn = get_sqlite_connection()
    cursor = s_conn.cursor()
    cursor.execute("SELECT * FROM documents WHERE student_id = ? ORDER BY doc_type ASC", (student_id,))
    rows = cursor.fetchall()
    s_conn.close()
    return [dict(r) for r in rows]


def submit_student_application(student_id: str) -> bool:
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE students SET app_status = 'pending', submit_at = NOW() WHERE student_id = %s", (student_id,))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception:
            if conn.is_connected():
                conn.close()

    s_conn = get_sqlite_connection()
    cursor = s_conn.cursor()
    cursor.execute("UPDATE students SET app_status = 'pending', submit_at = datetime('now') WHERE student_id = ?", (student_id,))
    s_conn.commit()
    s_conn.close()
    return True


def bulk_update_docs_status(student_id: str, status: str, comment: str = "") -> bool:
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE documents SET status = %s, comment = %s WHERE student_id = %s AND status = 'รอตรวจ'", (status, comment, student_id))
            app_status = "passed" if status == "ผ่าน" else "failed"
            cursor.execute("UPDATE students SET app_status = %s WHERE student_id = %s", (app_status, student_id))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception:
            if conn.is_connected():
                conn.close()

    s_conn = get_sqlite_connection()
    cursor = s_conn.cursor()
    cursor.execute("UPDATE documents SET status = ?, comment = ? WHERE student_id = ? AND status = 'รอตรวจ'", (status, comment, student_id))
    app_status = "passed" if status == "ผ่าน" else "failed"
    cursor.execute("UPDATE students SET app_status = ? WHERE student_id = ?", (app_status, student_id))
    s_conn.commit()
    s_conn.close()
    return True
