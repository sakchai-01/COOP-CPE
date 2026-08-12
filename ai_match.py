import os
import sys
import json
import warnings

warnings.filterwarnings("ignore")

import mysql.connector

from fastapi import FastAPI, Form, UploadFile, File
from typing import Optional

from openai import OpenAI


# =========================================================
# Configuration
# =========================================================

def load_env():
    env_path = os.path.join(
        os.path.dirname(__file__),
        ".env"
    )

    if os.path.exists(env_path):
        with open(
            env_path,
            "r",
            encoding="utf-8"
        ) as f:

            for line in f:

                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" in line:

                    key, value = line.split(
                        "=",
                        1
                    )

                    os.environ[key.strip()] = value.strip()


load_env()


# =========================================================
# Typhoon API Configuration
# =========================================================

API_KEY = os.environ.get(
    "TYPHOON_API_KEY"
)

MODEL = os.environ.get(
    "TYPHOON_MODEL",
    "typhoon-v2.5-30b-a3b-instruct"
)


if not API_KEY:

    print(
        json.dumps(
            {
                "error":
                "Missing TYPHOON_API_KEY in .env file"
            },
            ensure_ascii=False
        )
    )

    API_KEY = None


# =========================================================
# Typhoon Client
# =========================================================

client = None

if API_KEY:

    client = OpenAI(
        api_key=API_KEY,
        base_url="https://api.opentyphoon.ai/v1"
    )


# =========================================================
# FastAPI
# =========================================================

app = FastAPI(
    title="Cooperative Education AI Matching API"
)


# =========================================================
# Database Setup
# =========================================================

db_config = {
    "host": os.environ.get(
        "DB_HOST",
        "localhost"
    ),

    "user": os.environ.get(
        "DB_USER",
        "root"
    ),

    "password": os.environ.get(
        "DB_PASSWORD",
        ""
    ),

    "database": os.environ.get(
        "DB_NAME",
        "coop_db"
    ),

    "charset": "utf8mb4"
}


def get_db_connection():

    return mysql.connector.connect(
        **db_config
    )


# =========================================================
# Get Companies
# =========================================================

def get_companies():

    conn = get_db_connection()

    cursor = conn.cursor(
        dictionary=True
    )

    cursor.execute("""
        SELECT
            id,
            `ชื่อสถานประกอบการ` AS company_name,
            position,
            skills_required,
            interest_required,
            work_mode
        FROM companies
    """)

    companies = cursor.fetchall()

    cursor.close()
    conn.close()

    return companies


# =========================================================
# Build Company Information
# =========================================================

def build_company_text(companies):

    company_text = ""

    for index, company in enumerate(
        companies,
        start=1
    ):

        company_text += f"""

บริษัทลำดับที่ {index}

Company ID:
{company.get("id", "")}

ชื่อสถานประกอบการ:
{company.get("company_name", "")}

ตำแหน่ง:
{company.get("position", "")}

ทักษะที่บริษัทต้องการ:
{company.get("skills_required", "")}

ความสนใจที่บริษัทต้องการ:
{company.get("interest_required", "")}

รูปแบบการทำงาน:
{company.get("work_mode", "")}

--------------------------------
"""

    return company_text


# =========================================================
# AI Matching
# =========================================================

def get_match_reasoning(
    student_profile,
    companies,
    cv_path=None,
    port_path=None,
    cv_url=None,
    portfolio_url=None
):

    if not client:

        raise Exception(
            "ไม่พบ TYPHOON_API_KEY ในไฟล์ .env"
        )


    # -----------------------------------------------------
    # Company Data
    # -----------------------------------------------------

    company_text = build_company_text(
        companies
    )


    # -----------------------------------------------------
    # CV / Portfolio Information
    # -----------------------------------------------------

    file_information = ""


    if cv_path:

        file_information += f"""

นักศึกษามีไฟล์ CV:
{os.path.basename(cv_path)}

โปรดถือว่ามี CV ประกอบการวิเคราะห์
"""


    if port_path:

        file_information += f"""

นักศึกษามีไฟล์ Portfolio:
{os.path.basename(port_path)}

โปรดถือว่ามี Portfolio ประกอบการวิเคราะห์
"""


    if cv_url:

        file_information += """

นักศึกษามี CV ที่จัดเก็บอยู่ในระบบ Storage
"""


    if portfolio_url:

        file_information += """

นักศึกษามี Portfolio ที่จัดเก็บอยู่ในระบบ Storage
"""


    # -----------------------------------------------------
    # System Prompt
    # -----------------------------------------------------

    system_prompt = """
คุณคือ AI Job Matching Expert
ของระบบสหกิจศึกษา

หน้าที่ของคุณคือวิเคราะห์ความเหมาะสม
ระหว่างนักศึกษาและสถานประกอบการ

ให้พิจารณาข้อมูลดังต่อไปนี้:

1. Major / สาขาวิชา
2. GPA
3. Skills
4. Career Interest
5. Work Mode
6. ตำแหน่งที่บริษัทต้องการ
7. Skills ที่บริษัทต้องการ
8. Interest ที่บริษัทต้องการ
9. Work Mode ของบริษัท

หลักการให้คะแนน:

match_score คือ
คะแนนความเหมาะสมของนักศึกษากับบริษัท
0-100

chance_score คือ
คะแนนโอกาสที่โปรไฟล์นักศึกษาจะเหมาะกับตำแหน่งฝึกงาน
0-100

การให้คะแนนต้องมาจากข้อมูลจริง
ห้ามสุ่มคะแนน

หาก Major ตรงกับตำแหน่งหรือสายงาน
ให้พิจารณาคะแนนสูงขึ้น

หาก Skills ของนักศึกษาตรงกับ
skills_required
ให้พิจารณาคะแนนสูงขึ้น

หาก Career Interest ตรงกับ
interest_required
ให้พิจารณาคะแนนสูงขึ้น

หาก Work Mode ตรงกัน
ให้พิจารณาคะแนนเพิ่มขึ้น

หากข้อมูลไม่ตรงกัน
ให้ลดคะแนนตามความเหมาะสม

GPA ใช้เป็นข้อมูลประกอบ
แต่ไม่ควรเป็นปัจจัยเดียว

เลือกบริษัทที่เหมาะสมที่สุด 5 บริษัท

เรียงลำดับจากบริษัทที่เหมาะสมที่สุด
ไปยังบริษัทที่เหมาะสมน้อยกว่า

reason ต้องเป็นภาษาไทย

reason ต้องอธิบายจากข้อมูลจริง
และควรกล่าวถึงจุดที่ตรงกัน เช่น

- สาขา
- Skills
- Career Interest
- Work Mode
- ตำแหน่ง

ห้ามสร้างข้อมูลบริษัทขึ้นมาเอง

ห้ามสร้างข้อมูลนักศึกษาขึ้นมาเอง

ห้ามสุ่มบริษัท

ห้ามสุ่มคะแนน

ห้ามให้ทุกบริษัทคะแนนเท่ากัน


สำคัญมาก:

ให้ตอบกลับเป็น JSON เท่านั้น

ห้ามใส่ Markdown

ห้ามใส่ ```json

ห้ามใส่ข้อความก่อน JSON

ห้ามใส่ข้อความหลัง JSON


รูปแบบ JSON:

{
    "matches": [
        {
            "company_id": 1,
            "company_name": "ชื่อบริษัท",
            "match_score": 90,
            "chance_score": 85,
            "reason": "เหตุผลภาษาไทย"
        }
    ]
}
"""


    # -----------------------------------------------------
    # User Prompt
    # -----------------------------------------------------

    user_prompt = f"""
ข้อมูลนักศึกษา:

{student_profile}

{file_information}


ข้อมูลสถานประกอบการ:

{company_text}


โปรดวิเคราะห์ข้อมูลนักศึกษากับ
สถานประกอบการทั้งหมด

เลือก 5 บริษัทที่เหมาะสมที่สุด

เรียงลำดับจาก match_score สูงสุด
ไปต่ำสุด

ต้องตอบกลับเป็น JSON เท่านั้น
ตามรูปแบบที่กำหนด
"""


    # -----------------------------------------------------
    # Call Typhoon
    # -----------------------------------------------------

    try:

        response = client.chat.completions.create(

            model=MODEL,

            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],

            temperature=0.2,

            max_tokens=4000
        )


    except Exception as e:

        raise Exception(
            f"Typhoon API Error: {str(e)}"
        )


    # -----------------------------------------------------
    # Read Response
    # -----------------------------------------------------

    result_text = (
        response
        .choices[0]
        .message
        .content
        .strip()
    )


    # -----------------------------------------------------
    # Remove Markdown
    # -----------------------------------------------------

    if result_text.startswith("```"):

        result_text = result_text.replace(
            "```json",
            ""
        )

        result_text = result_text.replace(
            "```",
            ""
        )

        result_text = result_text.strip()


    # -----------------------------------------------------
    # Convert JSON
    # -----------------------------------------------------

    try:

        result = json.loads(
            result_text
        )

    except json.JSONDecodeError:

        start = result_text.find("{")
        end = result_text.rfind("}")

        if start != -1 and end != -1:

            result = json.loads(
                result_text[
                    start:end + 1
                ]
            )

        else:

            raise Exception(
                "Typhoon ส่งผลลัพธ์ไม่เป็น JSON: "
                + result_text
            )


    # -----------------------------------------------------
    # Check Result
    # -----------------------------------------------------

    if not isinstance(
        result,
        dict
    ):

        raise Exception(
            "ผลลัพธ์จาก Typhoon ไม่ถูกต้อง"
        )


    if "matches" not in result:

        raise Exception(
            "ไม่พบ matches จาก Typhoon"
        )


    return result


# =========================================================
# FastAPI /match
# =========================================================

@app.post("/match")
async def match_student(

    profile: str = Form(...),

    cv: Optional[
        UploadFile
    ] = File(None),

    portfolio: Optional[
        UploadFile
    ] = File(None),

    cv_url: Optional[
        str
    ] = Form(None),

    portfolio_url: Optional[
        str
    ] = Form(None)

):

    try:

        print("")
        print("====================================")
        print("TYHOON AI MATCH REQUEST")
        print("====================================")


        # -------------------------------------------------
        # Check API
        # -------------------------------------------------

        if not client:

            return {
                "error":
                "ไม่พบ TYPHOON_API_KEY ใน .env"
            }


        # -------------------------------------------------
        # Get Companies
        # -------------------------------------------------

        companies = get_companies()


        if not companies:

            return {
                "error":
                "No companies found in database"
            }


        print(
            "Companies:",
            len(companies)
        )


        # -------------------------------------------------
        # Temporary Files
        # -------------------------------------------------

        temp_dir = os.path.join(
            os.path.dirname(__file__),
            "uploads",
            "api_temp"
        )


        os.makedirs(
            temp_dir,
            exist_ok=True
        )


        cv_temp_path = None
        port_temp_path = None


        # -------------------------------------------------
        # Save CV
        # -------------------------------------------------

        if cv:

            cv_temp_path = os.path.join(
                temp_dir,
                "cv_temp.pdf"
            )


            with open(
                cv_temp_path,
                "wb"
            ) as f:

                content = await cv.read()

                f.write(content)


        # -------------------------------------------------
        # Save Portfolio
        # -------------------------------------------------

        if portfolio:

            port_temp_path = os.path.join(
                temp_dir,
                "portfolio_temp.pdf"
            )


            with open(
                port_temp_path,
                "wb"
            ) as f:

                content = await portfolio.read()

                f.write(content)


        # -------------------------------------------------
        # Run AI
        # -------------------------------------------------

        result = get_match_reasoning(

            student_profile=profile,

            companies=companies,

            cv_path=cv_temp_path,

            port_path=port_temp_path,

            cv_url=cv_url,

            portfolio_url=portfolio_url
        )


        print("")
        print("Typhoon Result:")

        print(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2
            )
        )


        # -------------------------------------------------
        # Delete Temporary Files
        # -------------------------------------------------

        try:

            if (
                cv_temp_path
                and os.path.exists(
                    cv_temp_path
                )
            ):

                os.remove(
                    cv_temp_path
                )


            if (
                port_temp_path
                and os.path.exists(
                    port_temp_path
                )
            ):

                os.remove(
                    port_temp_path
                )

        except Exception:

            pass


        return result


    except Exception as e:

        print("")
        print("====================================")
        print("AI ERROR")
        print("====================================")

        print(
            str(e)
        )


        return {
            "error": str(e)
        }


# =========================================================
# Run Directly
# =========================================================

if __name__ == "__main__":

    import argparse


    parser = argparse.ArgumentParser()


    parser.add_argument(
        "profile",
        nargs="?",
        help="Student profile text"
    )


    parser.add_argument(
        "--cv",
        help="Path to CV PDF",
        default=None
    )


    parser.add_argument(
        "--port",
        help="Path to Portfolio PDF",
        default=None
    )


    args = parser.parse_args()


    # -----------------------------------------------------
    # No Profile
    # -----------------------------------------------------

    if not args.profile:

        print(
            json.dumps(
                {
                    "error":
                    "Missing student profile"
                },
                ensure_ascii=False
            )
        )

        sys.exit(0)


    conn = None


    try:

        # -------------------------------------------------
        # Database
        # -------------------------------------------------

        conn = get_db_connection()

        cursor = conn.cursor(
            dictionary=True
        )


        cursor.execute("""
            SELECT
                id,
                `ชื่อสถานประกอบการ` AS company_name,
                position,
                skills_required,
                interest_required,
                work_mode
            FROM companies
        """)


        companies = cursor.fetchall()


        if not companies:

            print(
                json.dumps(
                    {
                        "error":
                        "No companies found"
                    },
                    ensure_ascii=False
                )
            )

            sys.exit(0)


        # -------------------------------------------------
        # AI
        # -------------------------------------------------

        final_result = get_match_reasoning(

            student_profile=args.profile,

            companies=companies,

            cv_path=args.cv,

            port_path=args.port
        )


        print(
            json.dumps(
                final_result,
                ensure_ascii=False
            )
        )


    except Exception as e:

        print(
            json.dumps(
                {
                    "error": str(e)
                },
                ensure_ascii=False
            )
        )


    finally:

        if conn:

            conn.close()