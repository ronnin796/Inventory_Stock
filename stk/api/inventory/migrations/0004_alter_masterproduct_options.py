
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0003_alter_product_sales_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="masterproduct",
            options={"verbose_name_plural": "Master Products"},
        ),
    ]
