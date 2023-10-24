# Generated by Django 4.1.9 on 2023-10-24 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apikeys', '0009_vmdata_end_time_full_vmdata_start_time_full_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vmdata',
            name='booted',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='vmdata',
            name='first_boot_time',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='vmdata',
            name='real_image_type',
            field=models.CharField(default='N/A', max_length=50),
        ),
    ]
