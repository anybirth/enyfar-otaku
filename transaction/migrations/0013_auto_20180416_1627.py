# Generated by Django 2.0.4 on 2018-04-16 07:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0012_remove_order_proposal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposal',
            name='item',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='itinerary',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='user',
        ),
        migrations.DeleteModel(
            name='Proposal',
        ),
    ]
