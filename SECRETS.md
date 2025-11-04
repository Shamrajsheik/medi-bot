## Secrets & API Key Rotation (quick reference)

This file explains what to do if an API key (or other secret) is leaked, how to rotate it safely, and how to remove secrets from git history.

Please follow these steps immediately if you see an error like "403 Your API key was reported as leaked":

1) Revoke/delete the compromised key
   - Open the Google Cloud Console → APIs & Services → Credentials.
   - Find the compromised API key and delete it (or disable it).

2) Create a new API key
   - Click "Create credentials" → "API key".
   - Name it something like `medi-bot-local`.

3) Restrict the new key (strongly recommended)
   - Under the API key's settings, set API restrictions: allow only the Generative AI / relevant API(s).
   - Add application restrictions where possible (HTTP referrers for web, IP addresses, or Android/iOS app restrictions).
   - Set usage quotas and alerts in the Cloud Console if available.

4) Update your local environment (.env)
   - Open the project's `.env` in the repo root and replace the `GOOGLE_API_KEY` value.
   - Format: `GOOGLE_API_KEY=YOUR_NEW_KEY` (no quotes, no surrounding spaces).
   - Do NOT commit `.env` to git. Add `.env` to `.gitignore` if it's not already ignored.

5) Verify the new key locally
   - Activate your virtual environment and run the diagnostic:

    ```powershell
    # from project root
    # activate venv (PowerShell)
    .\.venv\Scripts\Activate.ps1
    # install deps (if needed)
    pip install -r requirements.txt
    # run the diagnostic script
    python test_gemini_key.py
    ```

6) Restart the Streamlit app (same interpreter / venv)
    ```powershell
    python -m streamlit run app.py
    ```

If the key was ever committed to git, remove it from history (this rewrites history):

- Option A — BFG Repo-Cleaner (easier):
  1. Download the BFG jar and run (example):

    ```powershell
    # replace 'YOUR_SECRET' with the literal secret or use a file with sensitive patterns
    java -jar bfg.jar --replace-text passwords.txt
    # then follow BFG instructions to push rewritten history
    git reflog expire --expire=now --all
    git gc --prune=now --aggressive
    git push --force
    ```

- Option B — git filter-repo (recommended over filter-branch):
  - Install `git-filter-repo` (see its installation instructions) and run:

    ```powershell
    # example: remove all lines matching the secret value
    git filter-repo --replace-text replacements.txt
    # follow with garbage collection and force-push
    git push --force
    ```

Notes about history-rewrites
- Rewriting history and force-pushing will affect all collaborators and open PRs. Coordinate with your team before doing this.
- If the repo is on GitHub and the key was public, rotate the key regardless of history-rewriting — assume compromise.

Best practices
- Never store long-lived API keys in repository files. Use environment variables or a secrets manager (GitHub Actions Secrets, Azure Key Vault, Google Secret Manager, etc.).
- Use short-lived credentials where possible and rotate them frequently.
- Add `.env` to `.gitignore`.

If you want, I can:
- add `.env` to `.gitignore` if it's missing, or
- add a small safe helper script `scripts/update_env.py` that prompts for a key locally and writes `.env` (never prints or commits it).

---
Generated on: 2025-11-05
