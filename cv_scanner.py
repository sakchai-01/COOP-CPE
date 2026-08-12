import os
import sys
import json
import warnings

warnings.filterwarnings("ignore")

import google.generativeai as genai

# --- Configuration ---
def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

load_env()

def get_gemini_api_key():
    return os.environ.get('GEMINI_API_KEY')

def scan_pdf(file_path):
    try:
        api_key = get_gemini_api_key()
        if not api_key:
            return {"error": "Missing Gemini API Key"}

        genai.configure(api_key=api_key)

        # Check if file exists
        if not os.path.exists(file_path):
            return {"error": "File not found"}

        # Upload to Gemini File API
        # Or if it's small, we can try to extract text first, 
        # but Gemini 1.5 handles PDF natively well.
        
        # We'll use the upload method for PDF support
        myfile = genai.upload_file(file_path)
        
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        prompt = """
        Analyze this CV/Resume and extract information strictly in JSON format.
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
        
        Return ONLY valid JSON.
        """
        
        response = model.generate_content([prompt, myfile])
        
        # Clean response text (sometimes AI adds markdown blocks)
        text = response.text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
            
        return json.loads(text)
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No file path provided"}))
        sys.exit(0)
        
    pdf_path = sys.argv[1]
    result = scan_pdf(pdf_path)
    print(json.dumps(result, ensure_ascii=False))
