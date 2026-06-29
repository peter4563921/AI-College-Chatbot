import json
import re

import google.generativeai as genai

from backend.config import Config
from backend.models.kb_model import get_public_knowledge

INTENT_KEYWORDS = {
    "courses": [
        "course",
        "courses",
        "department",
        "branch",
        "cse",
        "computer science",
        "b.sc",
        "bsc",
        "b.e",
        "be",
        "b.tech",
        "btech",
        "ece",
        "eee",
        "mechanical",
        "civil",
        "mca",
        "mba",
        "biotech",
        "robotics",
        "artificial intelligence",
        "data science",
        "automobile",
        "biomedical",
        "electronics",
    ],
    "fees": [
        "fee",
        "fees",
        "tuition",
        "cost",
        "quota",
    ],
    "admission": [
        "admission",
        "apply",
        "join",
        "tnea",
        "document",
        "eligibility",
        "eligible",
    ],
    "hostel": [
        "hostel",
        "transport",
        "bus",
        "route",
        "wifi",
    ],
    "placements": [
        "placement",
        "placements",
        "company",
        "companies",
        "training",
        "internship",
        "recruitment",
    ],
    "scholarships": [
        "scholarship",
        "scholarships",
        "concession",
        "loan",
        "merit",
        "sports",
    ],
    "contact": [
        "contact",
        "phone",
        "email",
        "address",
        "location",
    ],
    "faculty": [
        "faculty",
        "staff",
        "professor",
        "teacher",
    ],
    "dates": [
        "date",
        "schedule",
        "last date",
        "opening",
        "commencement",
    ],
}

REFUSAL = (
    "Sorry, I can answer only questions related to the college "
    "knowledge base such as courses, fees, admission, eligibility, "
    "hostel, transport, placements, faculty, scholarships, "
    "contact details and important dates."
)


def detect_intent(message):
    text = message.lower()

    # Keyword matching
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return intent

    # Dynamic course detection from database
    try:
        knowledge = get_public_knowledge()

        for course in knowledge.get("courses", []):
            course_name = str(course.get("name", "")).lower()

            if course_name and course_name in text:
                return "courses"

    except Exception:
        pass

    return "unknown"


def compact_context(knowledge, intent):
    if intent == "unknown":
        return ""

    return json.dumps(
        knowledge,
        ensure_ascii=False,
        default=str,
    )[:12000]


def fallback_answer(message, knowledge, intent):

    if intent == "unknown":
        return REFUSAL

    labels = {
        "courses": "courses",
        "fees": "fees",
        "admission": "admissions",
        "hostel": "hostels",
        "placements": "placements",
        "scholarships": "scholarships",
        "contact": "contacts",
        "faculty": "faculty",
        "dates": "admissions",
    }

    rows = knowledge.get(labels.get(intent, ""), [])

    if not rows:
        return (
            "The requested information is not available in the current "
            "college knowledge base."
        )

    # Special handling for course-specific questions
    if intent == "courses":
        text = message.lower()

        for course in rows:
            name = str(course.get("name", "")).lower()

            if name and name in text:
                return "\n".join(
                    f"{key.replace('_', ' ').title()}: {value}"
                    for key, value in course.items()
                    if value not in (None, "", 0)
                )

    lines = []

    for row in rows[:8]:
        line = ", ".join(
            str(value)
            for value in row.values()
            if value not in (None, "", 0)
        )
        lines.append(line)

    return "\n".join(lines)


def generate_answer(message):

    intent = detect_intent(message)

    knowledge = get_public_knowledge()

    context = compact_context(knowledge, intent)

    if not context:
        return {
            "answer": REFUSAL,
            "intent": intent,
        }

    if not Config.GEMINI_API_KEY:
        return {
            "answer": fallback_answer(
                message,
                knowledge,
                intent,
            ),
            "intent": intent,
        }

    prompt = f"""
You are an AI College Enquiry Chatbot.

Answer ONLY using the knowledge base below.

If the user asks about a specific course, provide only that course's details.

If the answer is unavailable, reply:

"The information is not available in the current college knowledge base."

If the question is unrelated to the college, politely refuse.

Knowledge Base:
{context}

Question:
{message}
"""

    try:

        genai.configure(api_key=Config.GEMINI_API_KEY)

        model = genai.GenerativeModel(Config.GEMINI_MODEL)

        response = model.generate_content(prompt)

        answer = (
            re.sub(r"\n{3,}", "\n\n", response.text.strip())
            if response.text
            else ""
        )

        if not answer:
            answer = fallback_answer(
                message,
                knowledge,
                intent,
            )

        return {
            "answer": answer,
            "intent": intent,
        }

    except Exception:

        return {
            "answer": fallback_answer(
                message,
                knowledge,
                intent,
            ),
            "intent": intent,
        }