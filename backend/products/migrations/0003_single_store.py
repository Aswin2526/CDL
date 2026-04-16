from django.db import migrations, models


def migrate_vendor_to_store(apps, schema_editor):
    StoreSettings = apps.get_model("products", "StoreSettings")
    VendorProfile = apps.get_model("vendors", "VendorProfile")

    defaults = {
        "name": "ChitraBazar",
        "tagline": "Online painting gallery & store",
        "address": "",
        "phone": "",
        "email": "",
    }
    vendor = VendorProfile.objects.first()
    if vendor:
        defaults["name"] = vendor.shop_name or defaults["name"]
        defaults["address"] = vendor.address or ""
        defaults["phone"] = vendor.phone or ""
        if vendor.user_id:
            User = apps.get_model("users", "User")
            try:
                user = User.objects.get(pk=vendor.user_id)
                defaults["email"] = user.email
            except User.DoesNotExist:
                pass

    StoreSettings.objects.update_or_create(pk=1, defaults=defaults)


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0002_painting_fields"),
        ("vendors", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="StoreSettings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="ChitraBazar", max_length=200)),
                ("tagline", models.CharField(blank=True, max_length=255)),
                ("address", models.TextField(blank=True)),
                ("phone", models.CharField(blank=True, max_length=20)),
                ("email", models.EmailField(blank=True, max_length=254)),
            ],
            options={
                "verbose_name": "Store settings",
                "verbose_name_plural": "Store settings",
            },
        ),
        migrations.RunPython(migrate_vendor_to_store, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="product",
            name="vendor",
        ),
    ]
