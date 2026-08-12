import os
import secrets
import tempfile
import httpx
from pathlib import Path

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
SUPABASE_BUCKET = os.environ.get("SUPABASE_STORAGE_BUCKET", "coop-documents")


def is_supabase_ready() -> bool:
    if not SUPABASE_URL or not SUPABASE_KEY or not SUPABASE_BUCKET:
        return False
    if "your-project.supabase.co" in SUPABASE_URL or "your_service_role_key" in SUPABASE_KEY:
        return False
    return True


def upload_document(content_bytes: bytes, folder: str, original_filename: str) -> str:
    ext = Path(original_filename).suffix.lower() or ".pdf"
    clean_ext = ext.replace(".", "")
    filename = f"{secrets.token_hex(16)}.{clean_ext}"
    clean_folder = folder.strip("/")
    object_key = f"{clean_folder}/{filename}"

    # Try Supabase Storage if configured
    if is_supabase_ready():
        try:
            url = f"{SUPABASE_URL}/storage/v1/object/{SUPABASE_BUCKET}/{object_key}"
            headers = {
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "apikey": SUPABASE_KEY,
                "Content-Type": "application/pdf",
                "x-upsert": "true",
            }
            res = httpx.post(url, content=content_bytes, headers=headers, timeout=30)
            if 200 <= res.status_code < 300:
                return f"supabase://{SUPABASE_BUCKET}/{object_key}"
        except Exception as e:
            print(f"Supabase upload error: {e}")

    # Local / Serverless Temp Fallback
    temp_dir = Path(tempfile.gettempdir()) / "coop_uploads" / clean_folder
    temp_dir.mkdir(parents=True, exist_ok=True)
    target_path = temp_dir / filename
    target_path.write_bytes(content_bytes)

    return f"uploads/{clean_folder}/{filename}"


def get_signed_url(reference: str, expires_in: int = 900) -> str:
    if not reference.startswith("supabase://") or not is_supabase_ready():
        return reference

    rest = reference[len("supabase://"):]
    prefix = f"{SUPABASE_BUCKET}/"
    if not rest.startswith(prefix):
        return reference

    object_key = rest[len(prefix):]
    try:
        url = f"{SUPABASE_URL}/storage/v1/object/sign/{SUPABASE_BUCKET}/{object_key}"
        headers = {
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "apikey": SUPABASE_KEY,
            "Content-Type": "application/json",
        }
        res = httpx.post(url, json={"expiresIn": expires_in}, headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()
            if "signedURL" in data:
                return f"{SUPABASE_URL}/storage/v1{data['signedURL']}"
    except Exception as e:
        print(f"Supabase signed URL error: {e}")

    return reference
