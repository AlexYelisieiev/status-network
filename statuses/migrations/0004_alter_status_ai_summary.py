# Generated by Django 5.0 on 2023-12-25 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statuses', '0003_status_ai_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='ai_summary',
            field=models.TextField(default='', null=True),
        ),
    ]