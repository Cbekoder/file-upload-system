# Generated by Django 5.0.6 on 2024-05-30 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graphics', '0003_remove_file_to_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='category',
            name='is_done_required',
            field=models.BooleanField(default=False),
        ),
    ]
