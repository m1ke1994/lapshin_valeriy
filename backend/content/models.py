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
        "Язык",
        max_length=8,
        choices=LocaleChoices.choices,
        default=LocaleChoices.RU,
        help_text="ru или en",
    )
    title = models.CharField("Заголовок", max_length=255, blank=True, help_text="Заголовок блока (может быть пустым)")
    body = models.TextField("Текст/описание", blank=True, help_text="Основной текст или описание блока")
    extra = models.JSONField(
        "Дополнительные данные (JSON)",
        default=dict,
        blank=True,
        help_text="Доп. данные из translations.ts (labels, actions и т.д.)",
    )
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        unique_together = ("key", "locale")
        ordering = ["key", "locale"]
        verbose_name = "Контент-блок"
        verbose_name_plural = "Контент-блоки"

    def __str__(self) -> str:
        return f"{self.key} ({self.locale})"


class ProjectItem(models.Model):
    locale = models.CharField("Язык", max_length=8, choices=LocaleChoices.choices, default=LocaleChoices.RU)
    title = models.CharField("Название", max_length=255, help_text="Название проекта")
    description = models.TextField("Описание", blank=True)
    category = models.CharField("Категория", max_length=255, blank=True, help_text="Например: индустрия/тип проекта")
    stage = models.CharField("Стадия", max_length=255, blank=True, help_text="Например: MVP/пилот/серия")
    meta = models.CharField("Мета", max_length=255, blank=True, help_text="Короткая подпись/подзаголовок")
    tags = models.JSONField("Теги (JSON)", default=list, blank=True, help_text='Например: ["RS-485", "DALI"]')
    image = models.ImageField("Изображение", upload_to="projects/", blank=True, null=True)
    order = models.PositiveIntegerField("Порядок", default=0, help_text="Меньшее число — выше в списке")
    is_active = models.BooleanField("Активен", default=True, help_text="Показывать в публичном API")
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self) -> str:
        return self.title


class CertificateItem(models.Model):
    locale = models.CharField("Язык", max_length=8, choices=LocaleChoices.choices, default=LocaleChoices.RU)
    title = models.CharField("Название", max_length=255, blank=True, help_text="Подпись документа")
    subtitle = models.CharField("Подзаголовок", max_length=255, blank=True, help_text="Организация/мероприятие")
    type = models.CharField(
        "Тип",
        max_length=32,
        choices=CertificateType.choices,
        default=CertificateType.CERTIFICATE,
        help_text="Отзыв/диплом/сертификат",
    )
    image = models.ImageField("Изображение", upload_to="certificates/")
    order = models.PositiveIntegerField("Порядок", default=0, help_text="Меньшее число — выше в списке")
    is_active = models.BooleanField("Активен", default=True, help_text="Показывать в публичном API")
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Сертификат"
        verbose_name_plural = "Сертификаты"

    def __str__(self) -> str:
        return self.title or f"Certificate #{self.pk}"


class ContactRequest(models.Model):
    name = models.CharField("Имя", max_length=120)
    phone = models.CharField("Телефон", max_length=64)
    preferred_date = models.DateField("Дата", blank=True, null=True)
    preferred_time = models.TimeField("Время", blank=True, null=True)
    message = models.TextField("Комментарий", blank=True)
    locale = models.CharField(
        "Язык",
        max_length=8,
        choices=LocaleChoices.choices,
        default=LocaleChoices.RU,
        help_text="ru или en",
    )
    extra = models.JSONField(
        "Доп. данные (JSON)",
        default=dict,
        blank=True,
        help_text="Вспомогательные сведения (User-Agent, реферер и т.д.)",
    )
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заявка на контакт"
        verbose_name_plural = "Заявки на контакт"

    def __str__(self) -> str:
        return f"{self.name} ({self.phone})"
