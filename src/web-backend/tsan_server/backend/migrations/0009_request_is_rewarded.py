# Generated by Django 2.2.10 on 2020-05-28 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_paymentlog_log_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='is_rewarded',
            field=models.BooleanField(default=False),
        ),
    ]
