"""Pure helpers for bulk imports; preserve source text and flag contact-like text."""
import hashlib
import re

CONTACT_RULES = {
    "email_like": re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}"),
    "international_phone_like": re.compile(r"\+\d[\d ()-]{7,}\d"),
    "credential_like": re.compile(r"(?:AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9]{32,})"),
}


def flags(text):
    return [name for name, pattern in CONTACT_RULES.items() if pattern.search(text)]


def identity(kind, text, roman=None):
    value = kind + "\0" + text + ("\0" + roman if roman is not None else "")
    return hashlib.sha256(value.encode("utf-8")).hexdigest()
