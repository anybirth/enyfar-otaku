# Generated by Django 2.0.4 on 2018-04-12 08:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0005_remove_agreement_request'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='item',
        ),
        migrations.RemoveField(
            model_name='request',
            name='proposal',
        ),
        migrations.RemoveField(
            model_name='request',
            name='user',
        ),
        migrations.RemoveField(
            model_name='request',
            name='user_address',
        ),
        migrations.DeleteModel(
            name='Request',
        ),
    ]