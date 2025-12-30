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
    key = models.SlugField(
        "Ключ",
        max_length=120,
        help_text="Например: header, hero, values, approach, competencies, trust, projects, contacts, certificates",
    )
    locale = models.CharField(
        "Локаль",
        max_length=8,
        choices=LocaleChoices.choices,
        default=LocaleChoices.RU,
        help_text="ru или en",
    )
    title = models.CharField("Заголовок", max_length=255, blank=True, help_text="Заголовок секции (если есть)")
    body = models.TextField("Текст/описание", blank=True, help_text="Лид или основной текст секции")
    extra = models.JSONField(
        "Дополнительно (JSON)",
        default=dict,
        blank=True,
        help_text="Структура как в translations.ts: списки карточек, labels, actions и т.п.",
    )
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
    title = models.CharField("Название", max_length=255, help_text="Заголовок карточки")
    description = models.TextField("Описание", blank=True)
    category = models.CharField("Категория", max_length=255, blank=True, help_text="Например: отрасль/домен")
    stage = models.CharField("Стадия", max_length=255, blank=True, help_text="Например: MVP/пилот/серия")
    meta = models.CharField("Мета", max_length=255, blank=True, help_text="Короткая подпись, если нужна")
    tags = models.JSONField("Теги (JSON список)", default=list, blank=True, help_text='Пример: ["RS-485", "DALI"]')
    image = models.ImageField("Изображение", upload_to="projects/", blank=True, null=True)
    order = models.PositiveIntegerField("Порядок", default=0, help_text="Сортировка по возрастанию")
    is_active = models.BooleanField("Активен", default=True, help_text="Скрыть/показать на сайте")
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
    title = models.CharField("Название", max_length=255, blank=True, help_text="Короткий заголовок карточки")
    subtitle = models.CharField("Подзаголовок", max_length=255, blank=True, help_text="Описание/подпись")
    type = models.CharField(
        "Тип",
        max_length=32,
        choices=CertificateType.choices,
        default=CertificateType.CERTIFICATE,
        help_text="Определяет бейдж на карточке",
    )
    image = models.ImageField("Изображение", upload_to="certificates/")
    order = models.PositiveIntegerField("Порядок", default=0, help_text="Сортировка по возрастанию")
    is_active = models.BooleanField("Активен", default=True, help_text="Скрыть/показать на сайте")
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Сертификат"
        verbose_name_plural = "Сертификаты"

    def __str__(self) -> str:
        return self.title or f"Certificate #{self.pk}"
