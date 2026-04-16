from django.db import migrations, models


def convert_vendors_to_customers(apps, schema_editor):
    User = apps.get_model("users", "User")
    User.objects.filter(role="vendor").update(role="customer", is_vendor=False, is_customer=True)


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(convert_vendors_to_customers, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("admin", "Admin"),
                    ("customer", "Customer"),
                ],
                default="customer",
                max_length=20,
            ),
        ),
        migrations.RemoveField(
            model_name="user",
            name="is_vendor",
        ),
    ]
