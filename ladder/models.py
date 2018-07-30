from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from statistics import mode
import operator
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
import uuid
import os


def get_image_path(self, filename):
    """カスタマイズした画像パスを取得する.

    :param self: インスタンス (models.Model)
    :param filename: 元ファイル名
    :return: カスタマイズしたファイル名を含む画像パス
    """
    prefix = 'usericon/'
    name = str(uuid.uuid4()).replace('-', '')
    extension = os.path.splitext(filename)[-1]
    return prefix + name + extension


class UserManager(BaseUserManager):
    """ユーザーマネージャー."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """メールアドレスでの登録を必須にする"""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """is_staff(管理サイトにログインできるか)と、is_superuer(全ての権限)をFalseに"""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """スーパーユーザーは、is_staffとis_superuserをTrueに"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)





class User(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザーモデル."""
    name = models.CharField(_('表示用ユーザー名'),max_length=255)
    email = models.EmailField(_('email address'), unique=True)
    icon = models.ImageField(_('icon'),upload_to=get_image_path,blank=True,default=None)
    profile = models.TextField(_('profile'),blank=True)


    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_my_link(self):
        link_list = []
        return Link.objects.filter(user=self)

    def get_my_ladders(self):
        ladders_list = []
        for ladder in Ladder.objects.filter(user=self):
            ladders_list.append(ladder)
        return ladders_list

    @property
    def username(self):
        return self.email

    @property
    def user(self):
        return self.id



class Tag(models.Model):
    """タグ"""
    name = models.CharField('タグ名',max_length=50,unique=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Ladder(models.Model):
    """ラダー"""
    title = models.CharField('タイトル',max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name='投稿者',on_delete=models.CASCADE)
    created_at = models.DateTimeField('作成日',auto_now_add=True)
    update_at = models.DateTimeField('更新日',auto_now=True)
    is_public = models.BooleanField('公開設定',default=True)
    tags = models.ManyToManyField(Tag,related_name='tag',blank=True)

    class Meta:
        unique_together = ('user','title')


    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_unit(self):
        units_list = []
        for unit in Unit.objects.filter(ladder=self):
            units_list.append(unit)
        units_list.sort(key=operator.attrgetter('index'))
        return units_list

    def get_recommended_prev_ladder(self):
        prev_list = []
        for l_ladder in Link.objects.filter(latter=self):
            prev_list.append(l_ladder.prior)
        if prev_list:
            return mode(prev_list)
        else:
            return prev_list

    def get_recommended_next_ladder(self):
        next_list = []
        for p_ladder in Link.objects.filter(prior=self):
            next_list.append(p_ladder.latter)
        if next_list:
            return mode(next_list)
        else:
            return next_list

    def count_finish_number(self):
        units_list = self.get_unit()
        try:
            unit = units_list[-1]
            count = 0
            for ladder in LearningStatus.objects.filter(unit=unit):
                count += ladder.status
            return count
        except:
            return 0

    def count_learning_number(self):
        try:
            units_list = self.get_unit()
            first_unit = units_list[0]
            return LearningStatus.objects.all().filter(unit=first_unit).count()
        except:
            return 0;

    def units_number(self):
        units_list = self.get_unit()
        last_unit = units_list[-1]
        return last_unit.index

    def get_tags(self):
        return Tag.objects.all().filter(ladders=self)


class Unit(models.Model):
    """ユニット"""
    title = models.CharField('タイトル',max_length=40)
    description = models.TextField('説明文')
    ladder = models.ForeignKey(Ladder,related_name='units',on_delete=models.CASCADE)
    url = models.URLField('URL')
    index = models.PositiveIntegerField('番号')

    class Meta:
        unique_together = ('ladder','index')

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    @property
    def user(self):
        return self.ladder.user

    def get_comments(self):
        return Comment.objects.filter(unit=self)


class Link(models.Model):
    """リンク"""
    prior = models.ForeignKey(Ladder,related_name='prior_ladder',on_delete=models.CASCADE)
    latter = models.ForeignKey(Ladder,related_name='latter_ladder',on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,'ユーザー')

    class Meta:
        unique_together = ('user','latter')


    def __unicode__(self):
        return self.latter.title

    def __str__(self):
        return self.latter.title


class LearningStatus(models.Model):
    """学習状況"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name='ユーザー',on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit,verbose_name='ユニット',on_delete=models.CASCADE)
    status = models.BooleanField('学習状態')
    created_at = models.DateTimeField('作成日',default=timezone.now)
    update_at = models.DateTimeField('更新日',auto_now=True)

    class Meta:
        unique_together = ('user','unit')


    def __unicode__(self):
        return self.user.name+' '+self.unit.title

    def __str__(self):
        return self.user.name+' '+self.unit.title

    @property
    def ladder(self):
        return self.unit.ladder


class Comment(models.Model):
    """コメント"""
    unit = models.ForeignKey(Unit,verbose_name='ユニット',on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name='ユーザー',on_delete=models.CASCADE)
    text = models.TextField('コメント')
    target = models.ForeignKey('self',verbose_name='親コメント',blank=True,on_delete=models.CASCADE)
    created_at = models.DateTimeField('投稿日',default=timezone.now)

    def ___unicode__(self):
        return str(self.unit.pk)+(self.pk)

    def __str__(self):
        return str(self.unit.pk)+' '+str(self.pk)
