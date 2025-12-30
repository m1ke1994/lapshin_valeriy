from django.db import models
from django.utils.translation import gettext_lazy as _


class LocaleChoices(models.TextChoices):
    RU = "ru", _("Русский")
    EN = "en", _("English")


class CertificateType(models.TextChoices):
    REVIEW = "review", _("Отзыв")
    DIPLOMA = "diploma", _("Диплом")
    CERTIFICATE = "certificate", _("Сертификат")


class ContentBlock(models.Model):
    key = models.SlugField("Ключ", max_length=120)
    locale = models.CharField("Локаль", max_length=8, choices=LocaleChoices.choices, default=LocaleChoices.RU)
    title = models.CharField("Заголовок", max_length=255, blank=True)
    body = models.TextField("Текст", blank=True)
    extra = models.JSONField("Дополнительно (JSON)", default=dict, blank=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        unique_together = ("key", "locale")
        ordering = ["key", "locale"]
        verbose_name = "Блок контента"
        verbose_name_plural = "Блоки контента"

    def __str__(self) -> str:
        return f"{self.key} ({self.locale})"


class ProjectItem(models.Model):
    locale = models.CharField("Локаль", max_length=8, choices=LocaleChoices.choices, default=LocaleChoices.RU)
    title = models.CharField("Название", max_length=255)
    description = models.TextField("Описание", blank=True)
    category = models.CharField("Категория", max_length=255, blank=True)
    stage = models.CharField("Стадия", max_length=255, blank=True)
    meta = models.CharField("Мета", max_length=255, blank=True)
    tags = models.JSONField("Теги (JSON список)", default=list, blank=True)
    image = models.ImageField("Изображение", upload_to="projects/", blank=True, null=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активен", default=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self) -> str:
        return self.title


class CertificateItem(models.Model):
    locale = models.CharField("Локаль", max_length=8, choices=LocaleChoices.choices, default=LocaleChoices.RU)
    title = models.CharField("Название", max_length=255, blank=True)
    subtitle = models.CharField("Подзаголовок", max_length=255, blank=True)
    type = models.CharField(
        "Тип",
        max_length=32,
        choices=CertificateType.choices,
        default=CertificateType.CERTIFICATE,
    )
    image = models.ImageField("Изображение", upload_to="certificates/")
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активен", default=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Сертификат"
        verbose_name_plural = "Сертификаты"

    def __str__(self) -> str:
        return self.title or f"Certificate #{self.pk}"
