# Generated by Django 4.2.7 on 2023-12-03 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_book_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='thumbnail',
            field=models.URLField(max_length=9000, null=True),
        ),
    ]