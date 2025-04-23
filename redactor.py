import re
import sys
import os

# --- DEFAULTS ---
REPLACEMENT = "[REDACTED]"
DEFAULT_KEYWORDS_FILE = "keywords.txt"

# --- REGEX PATTERNS ---
IP_PATTERN = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'             # IPv4
VERSION_PATTERN = r'\b\d+(?:\.\d+){1,3}\b'              # Version numbers like 1.2.3
DOMAIN_PATTERN = r'\b[a-zA-Z0-9.-]+\.(com|org|net|edu|gov)\b'  # Domains

# --- FUNCTIONS ---

def load_keywords(filepath):
    """Loads keywords from a file, one per line."""
    if not os.path.isfile(filepath):
        print(f"⚠️ Keyword file not found: {filepath}")
        return []

    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def redact_text(text, keywords):
    """Redacts keywords and sensitive patterns from text."""
    for word in keywords:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        text = pattern.sub(REPLACEMENT, text)

    text = re.sub(IP_PATTERN, REPLACEMENT, text)
    text = re.sub(VERSION_PATTERN, REPLACEMENT, text)
    text = re.sub(DOMAIN_PATTERN, REPLACEMENT, text)

    return text

def main(transcript_path, keywords_path=DEFAULT_KEYWORDS_FILE):
    if not os.path.isfile(transcript_path):
        print(f"❌ File not found: {transcript_path}")
        sys.exit(1)

    keywords = load_keywords(keywords_path)
    if not keywords:
        print("⚠️ No keywords loaded. Continuing with pattern-based redaction only.")

    with open(transcript_path, "r", encoding="utf-8") as f:
        original = f.read()

    redacted = redact_text(original, keywords)

    redacted_file = transcript_path.replace(".txt", ".redacted.txt")
    with open(redacted_file, "w", encoding="utf-8") as f:
        f.write(redacted)

    print(f"✅ Redaction complete: {redacted_file}")

# --- ENTRY POINT ---
if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) == 0:
        print("Usage: python redactor.py <transcript.txt> [keywords.txt]")
        sys.exit(1)

    transcript_path = args[0]
    keywords_path = args[1] if len(args) > 1 else DEFAULT_KEYWORDS_FILE

    main(transcript_path, keywords_path)
