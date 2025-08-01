# Generated by Django 5.2.4 on 2025-07-29 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_rename_comment_review_review_text_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='review_text',
            new_name='comment',
        ),
        migrations.RemoveField(
            model_name='review',
            name='is_anonymous',
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]),
        ),
    ]
