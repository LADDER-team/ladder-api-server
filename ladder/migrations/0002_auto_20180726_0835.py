# Generated by Django 2.0.1 on 2018-07-26 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ladder', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='target',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ladder.Comment', verbose_name='親コメント'),
        ),
        migrations.AlterField(
            model_name='ladder',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='ladder.Tags', verbose_name='タグ'),
        ),
    ]
