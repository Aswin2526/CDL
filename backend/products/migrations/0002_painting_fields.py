# Generated manually for ChitraBazar painting catalog

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="artist_name",
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name="product",
            name="medium",
            field=models.CharField(
                choices=[
                    ("oil", "Oil"),
                    ("acrylic", "Acrylic"),
                    ("watercolor", "Watercolor"),
                    ("mixed", "Mixed Media"),
                    ("digital", "Digital Print"),
                    ("other", "Other"),
                ],
                default="oil",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="dimensions",
            field=models.CharField(blank=True, help_text="e.g. 24 × 36 in", max_length=80),
        ),
        migrations.AddField(
            model_name="product",
            name="is_framed",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="product",
            name="year_created",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
