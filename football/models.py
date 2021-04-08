from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from extensions.utils import datetime_to_jalali_str

# my managers

class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='P')

# my models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    picture = models.ImageField(upload_to='profile_images', verbose_name='تصویر')
    birthday = models.DateField(verbose_name='تاریخ تولد')

    class Meta:
        verbose_name = 'نویسنده'
        verbose_name_plural = 'نویسندگان'

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='عنوان')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='آدرس دسته بندی')
    position = models.IntegerField(verbose_name='جایگاه')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        ordering = ['position']

    def __str__(self):
        return self.name


class Article(models.Model):
    STATUS_CHOICES = (
        ('D', 'پیش نویس'),
        ('P', 'منتشر شده')
    )

    title = models.CharField(max_length=100, verbose_name='عنوان')
    author = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True,
        related_name='articles', verbose_name='نویسنده')
    content = models.TextField(verbose_name='محتوا')
    thumbnail = models.ImageField(upload_to='images', verbose_name='تصویر')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='آدرس مقاله')
    categories = models.ManyToManyField(Category, related_name='articles',
        verbose_name='دسته بندی ها')
    publish = models.DateTimeField(default=timezone.now, verbose_name='زمان انتشار')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='وضعیت')

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'

    def jpublish(self):
        return datetime_to_jalali_str(self.publish)
    jpublish.short_description = 'زمان انتشار'

    def __str__(self):
        return self.title

    objects = ArticleManager()
