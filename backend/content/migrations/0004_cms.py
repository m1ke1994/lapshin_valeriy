from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_update_labels'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name_ru', models.CharField(blank=True, max_length=255, verbose_name='Название сайта (RU)')),
                ('site_name_en', models.CharField(blank=True, max_length=255, verbose_name='Название сайта (EN)')),
                ('header_cta_text_ru', models.CharField(blank=True, max_length=255, verbose_name='Текст кнопки в шапке (RU)')),
                ('header_cta_text_en', models.CharField(blank=True, max_length=255, verbose_name='Текст кнопки в шапке (EN)')),
                ('header_cta_link', models.URLField(blank=True, verbose_name='Ссылка кнопки в шапке')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=64, verbose_name='Телефон')),
                ('address', models.CharField(blank=True, max_length=255, verbose_name='Адрес')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Изменено')),
            ],
            options={
                'verbose_name': 'Общие настройки',
                'verbose_name_plural': 'Общие настройки',
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('hero', 'Хиро'), ('values', 'Ценности'), ('approach', 'Подход'), ('competencies', 'Компетенции'), ('trust', 'Доверие'), ('projects', 'Проекты'), ('certificates', 'Сертификаты'), ('contacts', 'Контакты')], help_text='Выберите блок, который хотите отредактировать', max_length=32, verbose_name='Тип секции')),
                ('title_ru', models.CharField(blank=True, max_length=255, verbose_name='Заголовок (RU)')),
                ('title_en', models.CharField(blank=True, max_length=255, verbose_name='Заголовок (EN)')),
                ('subtitle_ru', models.CharField(blank=True, max_length=255, verbose_name='Подзаголовок (RU)')),
                ('subtitle_en', models.CharField(blank=True, max_length=255, verbose_name='Подзаголовок (EN)')),
                ('body_ru', models.TextField(blank=True, verbose_name='Основной текст (RU)')),
                ('body_en', models.TextField(blank=True, verbose_name='Основной текст (EN)')),
                ('button_text_ru', models.CharField(blank=True, max_length=255, verbose_name='Текст кнопки (RU)')),
                ('button_text_en', models.CharField(blank=True, max_length=255, verbose_name='Текст кнопки (EN)')),
                ('button_link', models.URLField(blank=True, verbose_name='Ссылка кнопки')),
                ('is_enabled', models.BooleanField(default=True, verbose_name='Показывать секцию')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Изменено')),
            ],
            options={
                'verbose_name': 'Раздел',
                'verbose_name_plural': 'Разделы сайта',
                'ordering': ['order', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_ru', models.CharField(max_length=255, verbose_name='Название (RU)')),
                ('title_en', models.CharField(blank=True, max_length=255, verbose_name='Название (EN)')),
                ('description_ru', models.TextField(blank=True, verbose_name='Описание (RU)')),
                ('description_en', models.TextField(blank=True, verbose_name='Описание (EN)')),
                ('category_ru', models.CharField(blank=True, max_length=255, verbose_name='Домен/категория (RU)')),
                ('category_en', models.CharField(blank=True, max_length=255, verbose_name='Домен/категория (EN)')),
                ('stage_ru', models.CharField(blank=True, max_length=255, verbose_name='Этап (RU)')),
                ('stage_en', models.CharField(blank=True, max_length=255, verbose_name='Этап (EN)')),
                ('tags_ru', models.CharField(blank=True, max_length=512, verbose_name='Теги (RU, через запятую)')),
                ('tags_en', models.CharField(blank=True, max_length=512, verbose_name='Теги (EN, comma separated)')),
                ('link', models.URLField(blank=True, verbose_name='Ссылка')),
                ('image', models.ImageField(blank=True, null=True, upload_to='projects/', verbose_name='Картинка')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                ('is_published', models.BooleanField(default=True, verbose_name='Показывать на сайте')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Изменено')),
            ],
            options={
                'verbose_name': 'Проект',
                'verbose_name_plural': 'Проекты',
                'ordering': ['order', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_ru', models.CharField(max_length=255, verbose_name='Название (RU)')),
                ('title_en', models.CharField(blank=True, max_length=255, verbose_name='Название (EN)')),
                ('issuer_ru', models.CharField(blank=True, max_length=255, verbose_name='Организация/выдавший (RU)')),
                ('issuer_en', models.CharField(blank=True, max_length=255, verbose_name='Организация/выдавший (EN)')),
                ('year', models.PositiveIntegerField(blank=True, null=True, verbose_name='Год')),
                ('description_ru', models.TextField(blank=True, verbose_name='Описание (RU)')),
                ('description_en', models.TextField(blank=True, verbose_name='Описание (EN)')),
                ('image', models.ImageField(blank=True, null=True, upload_to='certificates/', verbose_name='Изображение')),
                ('file', models.FileField(blank=True, null=True, upload_to='certificates/files/', verbose_name='Файл (PDF)')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                ('is_published', models.BooleanField(default=True, verbose_name='Показывать на сайте')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Изменено')),
            ],
            options={
                'verbose_name': 'Сертификат',
                'verbose_name_plural': 'Сертификаты',
                'ordering': ['order', 'id'],
            },
        ),
        migrations.CreateModel(
            name='SectionItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_type', models.CharField(choices=[('item', 'Пункт'), ('metric', 'Метрика'), ('note', 'Примечание')], default='item', help_text='Для хиро можно выбрать Метрика или Примечание', max_length=16, verbose_name='Тип пункта')),
                ('title_ru', models.CharField(blank=True, max_length=255, verbose_name='Заголовок/значение (RU)')),
                ('title_en', models.CharField(blank=True, max_length=255, verbose_name='Заголовок/значение (EN)')),
                ('text_ru', models.TextField(blank=True, verbose_name='Текст/подпись (RU)')),
                ('text_en', models.TextField(blank=True, verbose_name='Текст/подпись (EN)')),
                ('value_ru', models.CharField(blank=True, max_length=255, verbose_name='Доп. значение (RU)')),
                ('value_en', models.CharField(blank=True, max_length=255, verbose_name='Доп. значение (EN)')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                ('is_enabled', models.BooleanField(default=True, verbose_name='Показывать')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='content.section', verbose_name='Секция')),
            ],
            options={
                'verbose_name': 'Пункт списка',
                'verbose_name_plural': 'Пункты списков',
                'ordering': ['order', 'id'],
            },
        ),
    ]
