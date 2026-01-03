import json
from pathlib import Path

from django.core.management.base import BaseCommand

from content.models import Certificate, Project, Section, SectionItem, SectionItemType, SectionType, SiteSettings


DEFAULT_FILE = Path(__file__).resolve().parents[3] / "content" / "default_site_content.json"


def load_defaults():
    if DEFAULT_FILE.exists():
        return json.loads(DEFAULT_FILE.read_text(encoding="utf-8"))
    return {}


def get_locale(data, locale="ru"):
    return (data or {}).get(locale) or {}


class Command(BaseCommand):
    help = "Заполняет CMS данными из фронтового дефолта, чтобы сайт выглядел как сейчас."

    def handle(self, *args, **options):
        data = load_defaults()
        ru = get_locale(data, "ru")
        en = get_locale(data, "en")

        # Reset current CMS data
        SectionItem.objects.all().delete()
        Section.objects.all().delete()
        Project.objects.all().delete()
        Certificate.objects.all().delete()

        settings, _ = SiteSettings.objects.get_or_create(id=1)
        header_ru = ru.get("header", {})
        header_en = en.get("header", {})
        settings.site_name_ru = header_ru.get("logoTagline", "")
        settings.site_name_en = header_en.get("logoTagline", "")
        settings.header_cta_text_ru = header_ru.get("cta", "")
        settings.header_cta_text_en = header_en.get("cta", "")
        settings.header_cta_link = "#contacts"
        settings.email = "hello@ikb.studio"
        settings.save()

        order_counter = 0

        def add_section(section_type, sec_ru, sec_en):
            nonlocal order_counter
            section = Section.objects.create(
                type=section_type,
                title_ru=sec_ru.get("title", ""),
                title_en=sec_en.get("title", ""),
                subtitle_ru=sec_ru.get("eyebrow", ""),
                subtitle_en=sec_en.get("eyebrow", ""),
                body_ru=sec_ru.get("lead", sec_ru.get("body", "")),
                body_en=sec_en.get("lead", sec_en.get("body", "")),
                button_text_ru=(sec_ru.get("ctas") or {}).get("primary", ""),
                button_text_en=(sec_en.get("ctas") or {}).get("primary", ""),
                button_link="#contacts",
                order=order_counter,
            )
            order_counter += 1
            return section

        # Hero
        hero = add_section(SectionType.HERO, ru.get("hero", {}), en.get("hero", {}))
        for item in ru.get("hero", {}).get("metrics", []):
            SectionItem.objects.create(
                section=hero,
                item_type=SectionItemType.METRIC,
                title_ru=item.get("value", ""),
                text_ru=item.get("label", ""),
                title_en="",
                text_en="",
            )
        notes_ru = ru.get("hero", {}).get("notes", []) or []
        notes_en = en.get("hero", {}).get("notes", []) or []
        for idx, item in enumerate(notes_ru):
            pair = notes_en[idx] if idx < len(notes_en) else {}
            SectionItem.objects.create(
                section=hero,
                item_type=SectionItemType.NOTE,
                title_ru=item.get("title", ""),
                text_ru=item.get("body", ""),
                title_en=pair.get("title", ""),
                text_en=pair.get("body", ""),
            )

        # Values
        values = add_section(SectionType.VALUES, ru.get("values", {}), en.get("values", {}))
        for idx, card in enumerate(ru.get("values", {}).get("cards", [])):
            pair = (en.get("values", {}).get("cards", []) or [])
            pair_card = pair[idx] if idx < len(pair) else {}
            SectionItem.objects.create(
                section=values,
                item_type=SectionItemType.ITEM,
                title_ru=card.get("title", ""),
                text_ru=card.get("body", ""),
                title_en=pair_card.get("title", ""),
                text_en=pair_card.get("body", ""),
                order=idx,
            )

        # Approach
        approach = add_section(SectionType.APPROACH, ru.get("approach", {}), en.get("approach", {}))
        for idx, step in enumerate(ru.get("approach", {}).get("steps", [])):
            pair = (en.get("approach", {}).get("steps", []) or [])
            pair_step = pair[idx] if idx < len(pair) else {}
            SectionItem.objects.create(
                section=approach,
                item_type=SectionItemType.ITEM,
                title_ru=step.get("title", ""),
                text_ru=step.get("body", ""),
                title_en=pair_step.get("title", ""),
                text_en=pair_step.get("body", ""),
                order=idx,
            )

        # Competencies
        competencies = add_section(SectionType.COMPETENCIES, ru.get("competencies", {}), en.get("competencies", {}))
        for idx, card in enumerate(ru.get("competencies", {}).get("cards", [])):
            pair = (en.get("competencies", {}).get("cards", []) or [])
            pair_card = pair[idx] if idx < len(pair) else {}
            SectionItem.objects.create(
                section=competencies,
                item_type=SectionItemType.ITEM,
                title_ru=card.get("title", ""),
                text_ru=card.get("body", ""),
                title_en=pair_card.get("title", ""),
                text_en=pair_card.get("body", ""),
                order=idx,
            )

        # Trust
        trust = add_section(SectionType.TRUST, ru.get("trust", {}), en.get("trust", {}))
        for idx, card in enumerate(ru.get("trust", {}).get("cards", [])):
            pair = (en.get("trust", {}).get("cards", []) or [])
            pair_card = pair[idx] if idx < len(pair) else {}
            SectionItem.objects.create(
                section=trust,
                item_type=SectionItemType.ITEM,
                title_ru=card.get("title", ""),
                text_ru=card.get("body", ""),
                title_en=pair_card.get("title", ""),
                text_en=pair_card.get("body", ""),
                order=idx,
            )

        # Projects section
        projects_section = add_section(SectionType.PROJECTS, ru.get("projects", {}), en.get("projects", {}))
        project_cards_ru = ru.get("projects", {}).get("cards", []) or []
        project_cards_en = en.get("projects", {}).get("cards", []) or []
        for idx, card in enumerate(project_cards_ru):
            pair = project_cards_en[idx] if idx < len(project_cards_en) else {}
            tags_ru = ", ".join(card.get("tags", []) or [])
            tags_en = ", ".join(pair.get("tags", []) or [])
            Project.objects.create(
                title_ru=card.get("title", ""),
                title_en=pair.get("title", ""),
                description_ru=card.get("body", ""),
                description_en=pair.get("body", ""),
                category_ru=card.get("category", ""),
                category_en=pair.get("category", ""),
                stage_ru=card.get("stage", ""),
                stage_en=pair.get("stage", ""),
                tags_ru=tags_ru,
                tags_en=tags_en,
                link="",
                order=idx,
                is_published=True,
            )

        # Certificates section
        certificates_section = add_section(SectionType.CERTIFICATES, ru.get("certificates", {}), en.get("certificates", {}))
        cert_items_ru = ru.get("certificates", {}).get("items", []) or []
        cert_items_en = en.get("certificates", {}).get("items", []) or []
        for idx, cert in enumerate(cert_items_ru):
            pair = cert_items_en[idx] if idx < len(cert_items_en) else {}
            Certificate.objects.create(
                title_ru=cert.get("title", ""),
                title_en=pair.get("title", ""),
                issuer_ru=cert.get("subtitle", ""),
                issuer_en=pair.get("subtitle", ""),
                description_ru="",
                description_en="",
                image=None,
                order=idx,
                is_published=True,
            )

        # Contacts section
        add_section(SectionType.CONTACTS, ru.get("contacts", {}), en.get("contacts", {}))

        self.stdout.write(self.style.SUCCESS("CMS заполнена дефолтным контентом."))
