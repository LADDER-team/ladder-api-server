# Generated by Django 2.0.1 on 2018-07-16 07:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import ladder.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('name', models.CharField(max_length=255, verbose_name='表示用ユーザー名')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('icon', models.ImageField(blank=True, null=True, upload_to='', verbose_name='icon')),
                ('profile', models.TextField(blank=True, verbose_name='profile')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', ladder.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='コメント')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='投稿日')),
                ('target', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ladder.Comment', verbose_name='親コメント')),
            ],
        ),
        migrations.CreateModel(
            name='Ladder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='タイトル')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
                ('is_public', models.BooleanField(default=True, verbose_name='公開設定')),
            ],
        ),
        migrations.CreateModel(
            name='LearningStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(verbose_name='学習状態')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='作成日')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='latter_ladder', to='ladder.Ladder')),
                ('prior', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prior_ladder', to='ladder.Ladder')),
                ('user', models.ForeignKey(on_delete='ユーザー', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='タグ名')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40, verbose_name='タイトル')),
                ('description', models.TextField(verbose_name='説明文')),
                ('url', models.URLField(verbose_name='URL')),
                ('index', models.PositiveIntegerField(verbose_name='番号')),
                ('ladder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='units', to='ladder.Ladder')),
            ],
        ),
        migrations.AddField(
            model_name='learningstatus',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ladder.Unit', verbose_name='ユニット'),
        ),
        migrations.AddField(
            model_name='learningstatus',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー'),
        ),
        migrations.AddField(
            model_name='ladder',
            name='tags',
            field=models.ManyToManyField(blank=True, to='ladder.Tags', verbose_name='タグ'),
        ),
        migrations.AddField(
            model_name='ladder',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='投稿者'),
        ),
        migrations.AddField(
            model_name='comment',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ladder.Unit', verbose_name='ユニット'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー'),
        ),
        migrations.AlterUniqueTogether(
            name='unit',
            unique_together={('ladder', 'index')},
        ),
        migrations.AlterUniqueTogether(
            name='link',
            unique_together={('user', 'latter')},
        ),
        migrations.AlterUniqueTogether(
            name='learningstatus',
            unique_together={('user', 'unit')},
        ),
        migrations.AlterUniqueTogether(
            name='ladder',
            unique_together={('user', 'title')},
        ),
    ]
