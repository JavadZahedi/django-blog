from django import forms
from .models import Category, Article, UserProfile
from django.contrib.auth.models import User
from django.utils import timezone

class DateInput(forms.DateInput): #This is a widget
    input_type = 'date'


class DateTimeInput(forms.DateTimeInput): #This is a widget
    input_type = 'datetime-local'


class ArticleForm(forms.ModelForm):
    publish = forms.DateTimeField(initial=timezone.now, label='زمان انتشار')

    class Meta:
        model = Article
        fields = ('title', 'content', 'thumbnail', 'slug',
            'categories', 'publish', 'status')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='رمز عبور')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    birthday = forms.DateField(widget=DateInput, label='تاریخ تولد')

    class Meta:
        model = UserProfile
        fields = ('picture', 'birthday')