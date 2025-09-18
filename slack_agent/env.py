import os

# High level constants

BOT_NAME = "Archer"
STORAGE_TYPE = os.environ.get("STORAGE_TYPE", "file")
FILE_STORAGE_BASE_DIR = os.environ.get("FILE_STORAGE_BASE_DIR", "./data")

REDACTION_ENABLED = bool(os.environ.get("REDACTION_ENABLED", False))

# GitHub API configuration
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID", "")
GITHUB_CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET", "")
GITHUB_REDIRECT_URI = os.environ.get("GITHUB_REDIRECT_URI", "")

# Google API configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REFRESH_TOKEN = os.environ.get("GOOGLE_REFRESH_TOKEN", "")
GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN", "")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN", "")
SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET", "")


# Redaction patterns
#
REDACT_EMAIL_PATTERN = os.environ.get(
    "REDACT_EMAIL_PATTERN", r"\b[A-Za-z0-9.*%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)
REDACT_PHONE_PATTERN = os.environ.get(
    "REDACT_PHONE_PATTERN", r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
)
REDACT_CREDIT_CARD_PATTERN = os.environ.get(
    "REDACT_CREDIT_CARD_PATTERN", r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b"
)
REDACT_SSN_PATTERN = os.environ.get("REDACT_SSN_PATTERN", r"\b\d{3}[- ]?\d{2}[- ]?\d{4}\b")
# For REDACT_USER_DEFINED_PATTERN, the default will never match anything
REDACT_USER_DEFINED_PATTERN = os.environ.get("REDACT_USER_DEFINED_PATTERN", r"(?!)")
