# Generated by Django 2.2.11 on 2020-04-19 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_request_is_captcha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='is_captcha',
            field=models.BooleanField(default=False),
        ),
    ]
