# Generated by Django 3.2.18 on 2023-02-24 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_customer_identification_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='transfer',
            name='processing_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
