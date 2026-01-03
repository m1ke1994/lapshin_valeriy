from django.db import models
from django.utils.translation import gettext_lazy as _


class ContactRequest(models.Model):
    name = models.CharField("Имя", max_length=120)
    phone = models.CharField("Телефон", max_length=64)
    preferred_date = models.DateField("Дата", blank=True, null=True)
    preferred_time = models.TimeField("Время", blank=True, null=True)
    message = models.TextField("Комментарий", blank=True)
    locale = models.CharField("Язык", max_length=8, default="ru", help_text="Например: ru или en")
    extra = models.JSONField("Доп. данные (JSON)", default=dict, blank=True, help_text="Служебные данные формы")
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self) -> str:
        return f"{self.name} ({self.phone})"


class SectionType(models.TextChoices):
    HERO = "hero", _("Хиро")
    VALUES = "values", _("Ценности")
    APPROACH = "approach", _("Подход")
    COMPETENCIES = "competencies", _("Компетенции")
    TRUST = "trust", _("Доверие")
    PROJECTS = "projects", _("Проекты")
    CERTIFICATES = "certificates", _("Сертификаты")
    CONTACTS = "contacts", _("Контакты")


class SectionItemType(models.TextChoices):
    ITEM = "item", _("Пункт")
    METRIC = "metric", _("Метрика")
    NOTE = "note", _("Примечание")


class SiteSettings(models.Model):
    site_name_ru = models.CharField("Название сайта (RU)", max_length=255, blank=True)
    site_name_en = models.CharField("Название сайта (EN)", max_length=255, blank=True)
    header_cta_text_ru = models.CharField("Текст кнопки в шапке (RU)", max_length=255, blank=True)
    header_cta_text_en = models.CharField("Текст кнопки в шапке (EN)", max_length=255, blank=True)
    header_cta_link = models.URLField("Ссылка кнопки в шапке", blank=True)
    email = models.EmailField("Email", blank=True)
    phone = models.CharField("Телефон", max_length=64, blank=True)
    address = models.CharField("Адрес", max_length=255, blank=True)
    updated_at = models.DateTimeField("Изменено", auto_now=True)

    class Meta:
        verbose_name = "Общие настройки"
        verbose_name_plural = "Общие настройки"

    def __str__(self) -> str:
        return self.site_name_ru or "Настройки сайта"


class Section(models.Model):
    type = models.CharField(
        "Тип секции",
        max_length=32,
        choices=SectionType.choices,
        help_text="Выберите блок, который хотите отредактировать",
    )
    title_ru = models.CharField("Заголовок (RU)", max_length=255, blank=True)
    title_en = models.CharField("Заголовок (EN)", max_length=255, blank=True)
    subtitle_ru = models.CharField("Подзаголовок (RU)", max_length=255, blank=True)
    subtitle_en = models.CharField("Подзаголовок (EN)", max_length=255, blank=True)
    body_ru = models.TextField("Основной текст (RU)", blank=True)
    body_en = models.TextField("Основной текст (EN)", blank=True)
    button_text_ru = models.CharField("Текст кнопки (RU)", max_length=255, blank=True)
    button_text_en = models.CharField("Текст кнопки (EN)", max_length=255, blank=True)
    button_link = models.URLField("Ссылка кнопки", blank=True)
    is_enabled = models.BooleanField("Показывать секцию", default=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    updated_at = models.DateTimeField("Изменено", auto_now=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы сайта"

    def __str__(self) -> str:
        return f"{self.get_type_display()}: {self.title_ru or self.title_en}"


class SectionItem(models.Model):
    section = models.ForeignKey(Section, related_name="items", on_delete=models.CASCADE, verbose_name="Секция")
    item_type = models.CharField(
        "Тип пункта",
        max_length=16,
        choices=SectionItemType.choices,
        default=SectionItemType.ITEM,
        help_text="Для хиро можно выбрать Метрика или Примечание",
    )
    title_ru = models.CharField("Заголовок/значение (RU)", max_length=255, blank=True)
    title_en = models.CharField("Заголовок/значение (EN)", max_length=255, blank=True)
    text_ru = models.TextField("Текст/подпись (RU)", blank=True)
    text_en = models.TextField("Текст/подпись (EN)", blank=True)
    value_ru = models.CharField("Доп. значение (RU)", max_length=255, blank=True)
    value_en = models.CharField("Доп. значение (EN)", max_length=255, blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    is_enabled = models.BooleanField("Показывать", default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Пункт списка"
        verbose_name_plural = "Пункты списков"

    def __str__(self) -> str:
        return self.title_ru or self.title_en or f"Пункт #{self.pk}"


class Project(models.Model):
    title_ru = models.CharField("Название (RU)", max_length=255)
    title_en = models.CharField("Название (EN)", max_length=255, blank=True)
    description_ru = models.TextField("Описание (RU)", blank=True)
    description_en = models.TextField("Описание (EN)", blank=True)
    category_ru = models.CharField("Домен/категория (RU)", max_length=255, blank=True)
    category_en = models.CharField("Домен/категория (EN)", max_length=255, blank=True)
    stage_ru = models.CharField("Этап (RU)", max_length=255, blank=True)
    stage_en = models.CharField("Этап (EN)", max_length=255, blank=True)
    tags_ru = models.CharField("Теги (RU, через запятую)", max_length=512, blank=True)
    tags_en = models.CharField("Теги (EN, comma separated)", max_length=512, blank=True)
    link = models.URLField("Ссылка", blank=True)
    image = models.ImageField("Картинка", upload_to="projects/", blank=True, null=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    is_published = models.BooleanField("Показывать на сайте", default=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Изменено", auto_now=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self) -> str:
        return self.title_ru or f"Проект #{self.pk}"


class Certificate(models.Model):
    title_ru = models.CharField("Название (RU)", max_length=255)
    title_en = models.CharField("Название (EN)", max_length=255, blank=True)
    issuer_ru = models.CharField("Организация/выдавший (RU)", max_length=255, blank=True)
    issuer_en = models.CharField("Организация/выдавший (EN)", max_length=255, blank=True)
    year = models.PositiveIntegerField("Год", blank=True, null=True)
    description_ru = models.TextField("Описание (RU)", blank=True)
    description_en = models.TextField("Описание (EN)", blank=True)
    image = models.ImageField("Изображение", upload_to="certificates/", blank=True, null=True)
    file = models.FileField("Файл (PDF)", upload_to="certificates/files/", blank=True, null=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    is_published = models.BooleanField("Показывать на сайте", default=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Изменено", auto_now=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Сертификат"
        verbose_name_plural = "Сертификаты"

    def __str__(self) -> str:
        return self.title_ru or f"Сертификат #{self.pk}"
