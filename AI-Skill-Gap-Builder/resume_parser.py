import pdfplumber
import re


def extract_resume_text(pdf_file):

    text = ""

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


def is_resume(text):
    """Check if the extracted text looks like a resume."""
    if not text or len(text.strip()) < 50:
        return False

    text_lower = text.lower()

    # Common resume section headers
    resume_sections = [
        "education", "experience", "work experience", "skills",
        "projects", "certifications", "certification", "objective",
        "summary", "professional summary", "career objective",
        "qualifications", "achievements", "internship",
        "technical skills", "programming", "languages",
        "contact", "personal details", "personal information",
        "academic", "training", "hobbies", "interests",
        "references", "publications", "awards", "volunteer",
        "profile", "about me", "declaration"
    ]

    # Check for email pattern
    has_email = bool(re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text))

    # Check for phone pattern
    has_phone = bool(re.search(r'[\+]?[\d\s\-\(\)]{7,15}', text))

    # Count how many resume sections are found
    section_count = sum(1 for section in resume_sections if section in text_lower)

    # A resume should have at least 2 section headers and either email or phone
    if section_count >= 2 and (has_email or has_phone):
        return True

    # If many sections found, it's likely a resume even without contact info
    if section_count >= 4:
        return True

    return False

