# Generated by Django 5.2.4 on 2025-07-29 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='comment',
            new_name='review_text',
        ),
        migrations.AddField(
            model_name='review',
            name='is_anonymous',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
