from django.contrib import admin

from .models import Certificate, ContactRequest, Project, Section, SectionItem, SiteSettings


class SectionItemInline(admin.TabularInline):
    model = SectionItem
    extra = 0
    fields = (
        "item_type",
        "title_ru",
        "title_en",
        "text_ru",
        "text_en",
        "value_ru",
        "value_en",
        "order",
        "is_enabled",
    )
    ordering = ("order", "id")


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("get_type_display", "title_ru", "is_enabled", "order", "updated_at")
    list_filter = ("type", "is_enabled")
    ordering = ("order", "id")
    search_fields = ("title_ru", "title_en", "body_ru", "body_en")
    inlines = [SectionItemInline]
    fieldsets = (
        (None, {"fields": ("type", "is_enabled", "order")}),
        (
            "Тексты",
            {
                "fields": (
                    ("title_ru", "title_en"),
                    ("subtitle_ru", "subtitle_en"),
                    ("body_ru", "body_en"),
                )
            },
        ),
        (
            "Кнопка",
            {"fields": (("button_text_ru", "button_text_en"), "button_link")},
        ),
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title_ru", "is_published", "order", "updated_at")
    list_filter = ("is_published",)
    search_fields = ("title_ru", "title_en", "description_ru", "description_en")
    ordering = ("order", "id")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": (("title_ru", "title_en"), ("description_ru", "description_en"))}),
        ("Категории и этап", {"fields": (("category_ru", "category_en"), ("stage_ru", "stage_en"), ("tags_ru", "tags_en"))}),
        ("Медиа и ссылка", {"fields": ("image", "link")}),
        ("Показ", {"fields": ("is_published", "order")}),
        ("Служебное", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("title_ru", "is_published", "order", "updated_at")
    list_filter = ("is_published",)
    search_fields = ("title_ru", "title_en", "issuer_ru", "issuer_en")
    ordering = ("order", "id")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": (("title_ru", "title_en"), ("issuer_ru", "issuer_en"), "year")}),
        ("Описание", {"fields": (("description_ru", "description_en"),)}),
        ("Файлы", {"fields": ("image", "file")}),
        ("Показ", {"fields": ("is_published", "order")}),
        ("Служебное", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name_ru", "email", "phone", "updated_at")
    fieldsets = (
        (None, {"fields": (("site_name_ru", "site_name_en"), ("email", "phone", "address"))}),
        ("Кнопка в шапке", {"fields": (("header_cta_text_ru", "header_cta_text_en"), "header_cta_link")}),
    )


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "preferred_date", "preferred_time", "locale", "created_at")
    list_filter = ("locale",)
    search_fields = ("name", "phone", "message")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
