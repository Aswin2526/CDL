from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("vendors", "0001_initial"),
        ("products", "0003_single_store"),
        ("users", "0002_single_store_users"),
    ]

    operations = [
        migrations.DeleteModel(
            name="VendorProfile",
        ),
    ]
