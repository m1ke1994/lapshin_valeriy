from django.db import models


class LocaleChoices(models.TextChoices):
    RU = "ru", "Russian"
    EN = "en", "English"


class CertificateType(models.TextChoices):
    REVIEW = "review", "Review"
    DIPLOMA = "diploma", "Diploma"
    CERTIFICATE = "certificate", "Certificate"


class ContentBlock(models.Model):
    key = models.SlugField(max_length=120)
    locale = models.CharField(max_length=8, choices=LocaleChoices.choices, default=LocaleChoices.RU)
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    extra = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("key", "locale")
        ordering = ["key", "locale"]
        verbose_name = "Content block"
        verbose_name_plural = "Content blocks"

    def __str__(self) -> str:
        return f"{self.key} ({self.locale})"


class ProjectItem(models.Model):
    locale = models.CharField(max_length=8, choices=LocaleChoices.choices, default=LocaleChoices.RU)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=255, blank=True)
    stage = models.CharField(max_length=255, blank=True)
    meta = models.CharField(max_length=255, blank=True)
    tags = models.JSONField(default=list, blank=True)
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self) -> str:
        return self.title


class CertificateItem(models.Model):
    locale = models.CharField(max_length=8, choices=LocaleChoices.choices, default=LocaleChoices.RU)
    title = models.CharField(max_length=255, blank=True)
    subtitle = models.CharField(max_length=255, blank=True)
    type = models.CharField(
        max_length=32,
        choices=CertificateType.choices,
        default=CertificateType.CERTIFICATE,
    )
    image = models.ImageField(upload_to="certificates/")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Certificate"
        verbose_name_plural = "Certificates"

    def __str__(self) -> str:
        return self.title or f"Certificate #{self.pk}"
