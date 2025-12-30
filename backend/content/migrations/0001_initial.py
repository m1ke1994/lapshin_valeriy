from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ContentBlock",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("key", models.SlugField(max_length=120)),
                ("locale", models.CharField(choices=[("ru", "Russian"), ("en", "English")], default="ru", max_length=8)),
                ("title", models.CharField(blank=True, max_length=255)),
                ("body", models.TextField(blank=True)),
                ("extra", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Content block",
                "verbose_name_plural": "Content blocks",
                "ordering": ["key", "locale"],
                "unique_together": {("key", "locale")},
            },
        ),
        migrations.CreateModel(
            name="CertificateItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("locale", models.CharField(choices=[("ru", "Russian"), ("en", "English")], default="ru", max_length=8)),
                ("title", models.CharField(blank=True, max_length=255)),
                ("subtitle", models.CharField(blank=True, max_length=255)),
                ("type", models.CharField(choices=[("review", "Review"), ("diploma", "Diploma"), ("certificate", "Certificate")], default="certificate", max_length=32)),
                ("image", models.ImageField(upload_to="certificates/")),
                ("order", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Certificate",
                "verbose_name_plural": "Certificates",
                "ordering": ["order", "id"],
            },
        ),
        migrations.CreateModel(
            name="ProjectItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("locale", models.CharField(choices=[("ru", "Russian"), ("en", "English")], default="ru", max_length=8)),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                ("category", models.CharField(blank=True, max_length=255)),
                ("stage", models.CharField(blank=True, max_length=255)),
                ("meta", models.CharField(blank=True, max_length=255)),
                ("tags", models.JSONField(blank=True, default=list)),
                ("image", models.ImageField(blank=True, null=True, upload_to="projects/")),
                ("order", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Project",
                "verbose_name_plural": "Projects",
                "ordering": ["order", "id"],
            },
        ),
    ]
