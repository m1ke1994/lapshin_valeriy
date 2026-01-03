from django.db import migrations, models

import content.models


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0002_contactrequest"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="certificateitem",
            options={"ordering": ["order", "id"], "verbose_name": "Сертификат", "verbose_name_plural": "Сертификаты"},
        ),
        migrations.AlterModelOptions(
            name="contactrequest",
            options={"ordering": ["-created_at"], "verbose_name": "Заявка на контакт", "verbose_name_plural": "Заявки на контакт"},
        ),
        migrations.AlterModelOptions(
            name="contentblock",
            options={
                "ordering": ["key", "locale"],
                "verbose_name": "Контент-блок",
                "verbose_name_plural": "Контент-блоки",
                "unique_together": {("key", "locale")},
            },
        ),
        migrations.AlterModelOptions(
            name="projectitem",
            options={"ordering": ["order", "id"], "verbose_name": "Проект", "verbose_name_plural": "Проекты"},
        ),
        migrations.AlterField(
            model_name="certificateitem",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Создано"),
        ),
        migrations.AlterField(
            model_name="certificateitem",
            name="image",
            field=models.ImageField(upload_to="certificates/", verbose_name="Изображение"),
        ),
        migrations.AlterField(
            model_name="certificateitem",
            name="is_active",
            field=models.BooleanField(default=True, help_text="Показывать в публичном API", verbose_name="Активен"),
        ),
        migrations.AlterField(
            model_name="certificateitem",
            name="locale",
            field=models.CharField(choices=[("ru", "Русский"), ("en", "English")], default="ru", max_length=8, verbose_name="Язык"),
        ),
        migrations.AlterField(
            model_name="certificateitem",
            name="order",
            field=models.PositiveIntegerField(default=0, help_text="Меньшее число — выше в списке", verbose_name="Порядок"),
        ),
        migrations.AlterField(
            model_name="certificateitem",
            name="subtitle",
            field=models.CharField(blank=True, help_text="Организация/мероприятие", max_length=255, verbose_name="Подзаголовок"),
        ),
        migrations.AlterField(
            model_name="certificateitem",
            name="title",
            field=models.CharField(blank=True, help_text="Подпись документа", max_length=255, verbose_name="Название"),
        ),
        migrations.AlterField(
            model_name="certificateitem",
            name="type",
            field=models.CharField(
                choices=[("review", "Отзыв"), ("diploma", "Диплом"), ("certificate", "Сертификат")],
                default="certificate",
                help_text="Отзыв/диплом/сертификат",
                max_length=32,
                verbose_name="Тип",
            ),
        ),
        migrations.AlterField(
            model_name="certificateitem",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Обновлено"),
        ),
        migrations.AlterField(
            model_name="contactrequest",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Создано"),
        ),
        migrations.AlterField(
            model_name="contactrequest",
            name="extra",
            field=models.JSONField(blank=True, default=dict, help_text="Вспомогательные сведения (User-Agent, реферер и т.д.)", verbose_name="Доп. данные (JSON)"),
        ),
        migrations.AlterField(
            model_name="contactrequest",
            name="locale",
            field=models.CharField(choices=[("ru", "Русский"), ("en", "English")], default="ru", help_text="ru или en", max_length=8, verbose_name="Язык"),
        ),
        migrations.AlterField(
            model_name="contactrequest",
            name="message",
            field=models.TextField(blank=True, verbose_name="Комментарий"),
        ),
        migrations.AlterField(
            model_name="contactrequest",
            name="name",
            field=models.CharField(max_length=120, verbose_name="Имя"),
        ),
        migrations.AlterField(
            model_name="contactrequest",
            name="phone",
            field=models.CharField(max_length=64, verbose_name="Телефон"),
        ),
        migrations.AlterField(
            model_name="contactrequest",
            name="preferred_date",
            field=models.DateField(blank=True, null=True, verbose_name="Дата"),
        ),
        migrations.AlterField(
            model_name="contactrequest",
            name="preferred_time",
            field=models.TimeField(blank=True, null=True, verbose_name="Время"),
        ),
        migrations.AlterField(
            model_name="contentblock",
            name="body",
            field=models.TextField(blank=True, help_text="Основной текст или описание блока", verbose_name="Текст/описание"),
        ),
        migrations.AlterField(
            model_name="contentblock",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Создано"),
        ),
        migrations.AlterField(
            model_name="contentblock",
            name="extra",
            field=models.JSONField(blank=True, default=dict, help_text="Доп. данные из translations.ts (labels, actions и т.д.)", verbose_name="Дополнительные данные (JSON)"),
        ),
        migrations.AlterField(
            model_name="contentblock",
            name="key",
            field=models.SlugField(help_text="Например: header, hero, values, approach, competencies, trust, projects, contacts, certificates", max_length=120, verbose_name="Ключ"),
        ),
        migrations.AlterField(
            model_name="contentblock",
            name="locale",
            field=models.CharField(choices=[("ru", "Русский"), ("en", "English")], default="ru", help_text="ru или en", max_length=8, verbose_name="Язык"),
        ),
        migrations.AlterField(
            model_name="contentblock",
            name="title",
            field=models.CharField(blank=True, help_text="Заголовок блока (может быть пустым)", max_length=255, verbose_name="Заголовок"),
        ),
        migrations.AlterField(
            model_name="contentblock",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Обновлено"),
        ),
        migrations.AlterField(
            model_name="projectitem",
            name="category",
            field=models.CharField(blank=True, help_text="Например: индустрия/тип проекта", max_length=255, verbose_name="Категория"),
        ),
        migrations.AlterField(
            model_name="projectitem",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Создано"),
        ),
        migrations.AlterField(
            model_name="projectitem",
            name="description",
            field=models.TextField(blank=True, verbose_name="Описание"),
        ),
        migrations.AlterField(
            model_name="projectitem",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="projects/", verbose_name="Изображение"),
        ),
        migrations.AlterField(
            model_name="projectitem",
            name="is_active",
            field=models.BooleanField(default=True, help_text="Показывать в публичном API", verbose_name="Активен"),
        ),
        migrations.AlterField(
            model_name="projectitem",
            name="locale",
            field=models.CharField(choices=[("ru", "Русский"), ("en", "English")], default="ru", max_length=8, verbose_name="Язык"),
        ),
        migrations.AlterField(
            model_name="projectitem",
            name="meta",
            field=models.CharField(blank=True, help_text="Короткая подпись/подзаголовок", max_length=255, verbose_name="Мета"),
        ),
        migrations.AlterField(
            model_name="projectitem",
            name="order",
            field=models.PositiveIntegerField(default=0, help_text="Меньшее число — выше в списке", verbose_name="Порядок"),
        ),
        migrations.AlterField(
            model_name="projectitem",
            name="stage",
            field=models.CharField(blank=True, help_text="Например: MVP/пилот/серия", max_length=255, verbose_name="Стадия"),
        ),
        migrations.AlterField(
            model_name="projectitem",
            name="tags",
            field=models.JSONField(blank=True, default=list, help_text='Например: ["RS-485", "DALI"]', verbose_name="Теги (JSON)"),
        ),
        migrations.AlterField(
            model_name="projectitem",
            name="title",
            field=models.CharField(help_text="Название проекта", max_length=255, verbose_name="Название"),
        ),
        migrations.AlterField(
            model_name="projectitem",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Обновлено"),
        ),
    ]
