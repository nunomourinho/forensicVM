# Generated by Django 4.1.2 on 2023-02-19 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='forensicVM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('forensicImage', models.CharField(max_length=30)),
                ('osDetected', models.BooleanField()),
                ('vncHost', models.CharField(max_length=30)),
                ('vncPort', models.IntegerField()),
            ],
        ),
    ]