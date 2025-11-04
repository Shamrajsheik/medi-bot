"""Quick tester for Google Generative AI (Gemini) API key.

Usage: python test_gemini_key.py

This script loads the `GOOGLE_API_KEY` from the environment (or .env),
configures the `google.generativeai` client, and makes a light request
to detect invalid / leaked / revoked keys. It prints actionable guidance
if a 403 leaked-key response is received.
"""
import os
import sys
import traceback
from dotenv import load_dotenv

try:
    import google.generativeai as genai
except Exception as e:
    print("The package 'google-generativeai' is not installed or failed to import:", e)
    print("Install with: python -m pip install google-generativeai")
    sys.exit(2)


def mask_key(key: str) -> str:
    if not key:
        return "<empty>"
    if len(key) <= 8:
        return key
    return f"{key[:4]}...{key[-4:]}"


def main():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    print("GOOGLE_API_KEY present:", bool(api_key))
    print("Masked value:", mask_key(api_key))

    if not api_key:
        print("No API key found in environment. Please set GOOGLE_API_KEY in your .env or environment.")
        sys.exit(1)

    try:
        genai.configure(api_key=api_key)
        print("Configured google.generativeai client.")
    except Exception as e:
        print("Error configuring client:", e)
        traceback.print_exc()
        sys.exit(3)

    # Make a lightweight request to check key validity. Listing models is safe and read-only.
    try:
        models_gen = genai.list_models()
        # Some client versions return a generator; convert to list safely
        try:
            models = list(models_gen)
        except TypeError:
            # If it's not iterable to list (unlikely), fall back to the original object
            models = models_gen

        num = len(models) if hasattr(models, "__len__") else "unknown"
        print(f"Retrieved {num} models. Showing up to first 10 (if available):")
        count = 0
        for m in models:
            if count >= 10:
                break
            # model object shape may vary by client version
            name = getattr(m, "name", None) or getattr(m, "model", None) or str(m)
            print(" -", name)
            count += 1
        print("Key appears valid for listing models.")
        sys.exit(0)
    except Exception as e:
        text = str(e)
        print("Request failed:", text)
        # Provide actionable advice for the leaked-key 403 case
        if "403" in text or "leaked" in text.lower() or "reported as leaked" in text.lower():
            print("\nDetected a 403/leaked-key response. Actions to take:")
            print("1) Immediately revoke or delete the compromised API key in the Google Cloud Console.")
            print("2) Create a new API key and restrict it: specify allowed IPs, referrers, and limit which APIs it can call.")
            print("3) Update your local .env with the new key and do NOT commit it to version control.")
            print("4) If the old key was committed to git, remove it from history (use the BFG or git filter-repo) and rotate any other secrets that were exposed.")
            print("5) For testing locally, run: python -m pip install python-dotenv google-generativeai && python test_gemini_key.py")
            sys.exit(4)

        # Other errors: show traceback to help debugging
        traceback.print_exc()
        sys.exit(5)


if __name__ == "__main__":
    main()
