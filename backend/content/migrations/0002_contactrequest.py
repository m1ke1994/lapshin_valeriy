from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ContactRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, verbose_name="گ?گ?‘?")),
                ("phone", models.CharField(max_length=64, verbose_name="گ÷گçگ>گç‘\"گ?گ?")),
                ("preferred_date", models.DateField(blank=True, null=True, verbose_name="گ\"گø‘'گø")),
                ("preferred_time", models.TimeField(blank=True, null=True, verbose_name="گ'‘?گçگ?‘?")),
                ("message", models.TextField(blank=True, verbose_name="گ÷گçگَ‘?‘'/گ?گُگٌ‘?گّگ?گٌگç")),
                (
                    "locale",
                    models.CharField(
                        choices=[("ru", "Russian"), ("en", "English")],
                        default="ru",
                        help_text="ru گٌگ>گٌ en",
                        max_length=8,
                        verbose_name="گ>گ?گَگّگ>‘?",
                    ),
                ),
                (
                    "extra",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        help_text="گ?گّگَگ+‘?گٌگ?گçگ? گِگ?گ+گ?گ?گ?گ>گçگ?گ?‘? گ?گّگَ گَگّگ?گُگٌ‘?گ؟گ?گçگ?گ? گُگ?گ?گُگٌ‘?‘?",
                        verbose_name="گ\"گ?گُگ?گ>گ?گٌ‘'گçگ>‘?گ?گ?",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="گِگ?گْگ?گّگ?گ?")),
            ],
            options={
                "verbose_name": "گ?گçگّگ?گًگ؟",
                "verbose_name_plural": "گ?گçگّگ?گًگ؟‘<",
                "ordering": ["-created_at"],
            },
        ),
    ]
