# Generated by Django 2.0.1 on 2018-10-03 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ladder', '0005_auto_20180811_0539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
    ]
