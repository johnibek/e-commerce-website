# Generated by Django 5.0.3 on 2024-03-29 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, null=True),
        ),
    ]
