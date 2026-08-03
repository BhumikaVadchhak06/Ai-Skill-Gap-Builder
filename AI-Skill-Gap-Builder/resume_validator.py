def is_resume(text):
    text = text.lower()

    resume_keywords = [
        "education",
        "experience",
        "skills",
        "projects",
        "objective",
        "summary",
        "certification",
        "internship",
        "technical skills",
        "work experience",
        "achievements",
        "contact",
        "email",
        "phone"
    ]

    score = 0

    for keyword in resume_keywords:
        if keyword in text:
            score += 1

    # Agar 3 ya usse zyada keywords mil jaye to resume maan lo
    return score >= 3
