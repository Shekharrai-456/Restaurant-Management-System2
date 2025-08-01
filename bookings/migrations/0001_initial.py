# Generated by Django 5.2.4 on 2025-07-26 11:36

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('booked_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
