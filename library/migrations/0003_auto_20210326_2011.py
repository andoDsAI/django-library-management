# Generated by Django 3.1.7 on 2021-03-26 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0002_fine_issue"),
    ]

    operations = [
        migrations.AlterField(
            model_name="issue",
            name="issued_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="issue",
            name="return_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]