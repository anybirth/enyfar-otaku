# Generated by Django 2.0.2 on 2018-03-04 23:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20180304_0848'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(blank=True, null=True, verbose_name='UUID'),
        ),
        migrations.AddField(
            model_name='user',
            name='uuid_deadline',
            field=models.DateTimeField(blank=True, null=True, verbose_name='token deadline'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, unique=True, validators=[django.core.validators.RegexValidator(message='電話番号はハイフンを除いた半角数字で入力してください。', regex='^[0-9]+$')], verbose_name='電話番号'),
        ),
    ]
