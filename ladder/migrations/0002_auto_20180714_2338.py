# Generated by Django 2.0.1 on 2018-07-14 23:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ladder', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ladder',
            old_name='creater',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='comment',
            name='target',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ladder.Comment', verbose_name='親コメント'),
        ),
        migrations.AlterUniqueTogether(
            name='ladder',
            unique_together={('user', 'title')},
        ),
    ]
