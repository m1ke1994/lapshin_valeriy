import copy
from typing import Dict, Optional

from .models import ContentBlock

DEFAULT_HOME = {
    "header": {
        "logoTagline": "Engineering bureau",
        "nav": ["Values", "Method", "Capabilities", "Trust", "Projects", "Contacts"],
        "cta": "Book a call",
        "menuTitle": "Navigation",
        "menuClose": "Close",
        "menuOpenLabel": "Open menu",
        "languageLabel": "Change language",
        "languageShort": {"ru": "RU", "en": "EN"},
    },
    "hero": {
        "eyebrow": "IKB — contract engineering & R&D",
        "title": "We design and ship engineered products to market.",
        "lead": "End-to-end engineering lane: concepts, mechanics, electronics, firmware, validation, and pre-series.",
        "ctas": {"primary": "Schedule a call", "secondary": "View projects"},
        "metrics": [],
        "notes": [],
    },
    "values": {
        "eyebrow": "IKB philosophy",
        "title": "Innovation, confidentiality, safety. Turning ideas into serial products.",
        "cards": [],
    },
    "approach": {
        "eyebrow": "Method",
        "title": "One integrated team: consulting, R&D, series handover.",
        "lead": "",
        "steps": [],
    },
    "competencies": {
        "eyebrow": "Capabilities",
        "title": "A full range of engineering skills in one lead center.",
        "cards": [],
    },
    "trust": {
        "eyebrow": "Trust",
        "title": "We serve industry leaders under NDA.",
        "lead": "",
        "cards": [],
    },
    "projects": {
        "eyebrow": "Projects",
        "title": "Domains where we deliver to market.",
        "lead": "",
        "labels": {
            "domain": "Domain",
            "stage": "Stage",
            "searchLabel": "Search",
            "search": "Search title, description, tags",
            "reset": "Reset",
            "empty": "No projects for the selected filters",
            "results": "Found",
        },
        "items": [],
    },
    "contacts": {
        "eyebrow": "Contacts",
        "title": "We will schedule a call within 48 hours.",
        "lead": "",
        "formTitle": "Book a consultation",
        "fields": {
            "name": {"label": "Name", "placeholder": "How should we address you?"},
            "phone": {"label": "Phone", "placeholder": "+1 (___) ___-__-__"},
            "date": {"label": "Date", "placeholder": ""},
            "time": {"label": "Time", "placeholder": ""},
        },
        "note": "",
        "button": "Send request",
        "alt": "Or email:",
        "mailSubject": "Consultation request — IKB",
        "mailLabels": {"name": "Name", "phone": "Phone", "date": "Date", "time": "Time"},
    },
    "certificates": {
        "eyebrow": "Credentials",
        "title": "Certificates & Awards",
        "lead": "",
        "type_labels": {"review": "Review", "diploma": "Diploma", "certificate": "Certificate"},
        "actions": {"close": "Close", "prev": "Previous", "next": "Next"},
        "items": [],
    },
}


def build_section(section_key: str, block: Optional[ContentBlock]) -> Dict:
    section = copy.deepcopy(DEFAULT_HOME.get(section_key, {}))
    if not block:
        return section

    # Map common fields to keep admin-friendly editing.
    if "title" in section and block.title:
        section["title"] = block.title
    if "lead" in section and block.body:
        section["lead"] = block.body
    elif "body" in section and block.body:
        section["body"] = block.body

    if isinstance(block.extra, dict):
        section.update(block.extra)

    return section


def collect_sections(blocks: Dict[str, ContentBlock]) -> Dict:
    return {key: build_section(key, blocks.get(key)) for key in DEFAULT_HOME.keys()}
