# Set up Supabase Storage

The application stores future CVs, portfolios, and supporting documents in the private `coop-documents` bucket. MySQL stores a `supabase://...` object reference, not the file itself.

1. Create a Supabase project.
2. In **Storage**, create a bucket named `coop-documents` and leave **Public bucket** turned off.
3. In **Project Settings > API**, copy the Project URL and the `service_role` key.
4. Add these values to the production `.env` in the same directory as `config.php`:

   ```env
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
   SUPABASE_STORAGE_BUCKET=coop-documents
   ```

5. For FastAPI, set the same `SUPABASE_URL` environment variable. It needs it only to validate short-lived signed URLs before downloading CVs for AI analysis.

Never expose `SUPABASE_SERVICE_ROLE_KEY` in JavaScript, HTML, a public repository, or a browser request. `.htaccess` blocks direct access to `.env` on Apache, but server-managed environment variables are preferable when available.

Existing files under `uploads/` remain readable through their old links. New uploads go to Supabase. Migrating old files can be done separately after Supabase is connected.
