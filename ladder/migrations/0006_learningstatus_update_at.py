# Generated by Django 2.0.1 on 2018-07-02 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ladder', '0005_auto_20180701_0441'),
    ]

    operations = [
        migrations.AddField(
            model_name='learningstatus',
            name='update_at',
            field=models.DateTimeField(auto_now=True, verbose_name='更新日'),
        ),
    ]
