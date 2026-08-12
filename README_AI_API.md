# Python AI API

PHP now calls a FastAPI service over HTTP instead of running Python with `shell_exec()`. The service uses Typhoon 2.5 for Thai matching and Typhoon OCR for PDF extraction.

## Local setup

1. Create and activate a virtual environment.
2. Install the packages:

   ```powershell
   py -m pip install -r requirements-ai.txt
   ```

3. Copy `.env.example` to `.env`, then set `TYPHOON_API_KEY`. For production, also set a long `AI_SERVICE_TOKEN` in the environment of both PHP and FastAPI.
4. Start the service from this project folder:

   ```powershell
   py -m uvicorn ai_api:app --host 127.0.0.1 --port 8000
   ```

5. Open `http://127.0.0.1:8000/health`; it should return `{"status":"ok"}`.

PHP uses `AI_SERVICE_URL` when supplied, otherwise it calls `http://127.0.0.1:8000`. It uses `AI_SERVICE_TOKEN` when supplied.

## Supabase Storage

Create a **private** Storage bucket named `coop-documents`. Set `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, and `SUPABASE_STORAGE_BUCKET` in the PHP and FastAPI environments. The service-role key remains on the server; file pages generate a 15-minute signed URL only when someone opens a file.

## Production

Host FastAPI separately (for example, a VM/container service). Configure `AI_SERVICE_URL` in PHP to that private HTTPS URL, and set the same `AI_SERVICE_TOKEN` for both services. Do not expose the FastAPI port publicly without authentication and HTTPS.
