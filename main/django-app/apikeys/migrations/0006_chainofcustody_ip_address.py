# Generated by Django 4.1.9 on 2023-10-12 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apikeys', '0005_chainofcustody'),
    ]

    operations = [
        migrations.AddField(
            model_name='chainofcustody',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
    ]