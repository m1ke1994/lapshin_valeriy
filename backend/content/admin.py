from django.contrib import admin

from .models import CertificateItem, ContactRequest, ContentBlock, ProjectItem


@admin.register(ContentBlock)
class ContentBlockAdmin(admin.ModelAdmin):
    list_display = ("key", "locale", "title", "updated_at")
    list_filter = ("locale",)
    search_fields = ("key", "title", "body")
    ordering = ("key", "locale")


@admin.register(ProjectItem)
class ProjectItemAdmin(admin.ModelAdmin):
    list_display = ("title", "locale", "order", "is_active", "updated_at")
    list_filter = ("locale", "is_active")
    search_fields = ("title", "description", "category", "stage")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("order", "id")


@admin.register(CertificateItem)
class CertificateItemAdmin(admin.ModelAdmin):
    list_display = ("title", "locale", "type", "order", "is_active")
    list_filter = ("locale", "type", "is_active")
    search_fields = ("title", "subtitle")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("order", "id")


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "preferred_date", "preferred_time", "locale", "created_at")
    list_filter = ("locale",)
    search_fields = ("name", "phone", "message")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
