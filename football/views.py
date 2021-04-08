from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Category, Article, UserProfile
from django.core.paginator import Paginator
from .forms import ArticleForm, UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from datetime import datetime

# Create your helper functions here.

def visitor_cookie_handler(request, response):
    visits = int(request.COOKIES.get('visits', '1'))
    last_visit_cookie = request.COOKIES.get('last_visit' ,str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).seconds > 0:
        visits += 1
        response.set_cookie('last_visit', str(datetime.now()))
    else:
        response.set_cookie('last_visit', last_visit_cookie)    
    response.set_cookie('visits', visits)


# Create your views here.

def home(request):
    article_list = Article.objects.published()
    paginator = Paginator(article_list, 3)
    page_number = request.GET.get('page', 1)
    articles = paginator.get_page(page_number)
    context = {
        'articles': articles,
        'active': 'home'
    }
    response = render(request, 'football/home.html', context)
    visitor_cookie_handler(request, response)
    return response


def article(request, slug):
    context = {
        'article': get_object_or_404(Article.objects.published(), slug=slug),
        'active': None
    }
    return render(request, 'football/article.html', context)


def category(request, slug):
    category_obj = get_object_or_404(Category, slug=slug)
    article_list = category_obj.articles.published()
    paginator = Paginator(article_list, 3)
    page_number = request.GET.get('page', 1)
    articles = paginator.get_page(page_number)
    context = {
        'articles': articles,
        'active': slug
    }
    return render(request, 'football/home.html', context)


@login_required
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user.profile
            form.save(commit=True)
            return HttpResponseRedirect('/football')
        else:
            pass
            #print(form.errors)
    else:
        form = ArticleForm()
    
    context = {'form': form}
    return render(request, 'football/add_article.html', context)


def sign_up(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user        
            profile.save()
            login(request, user)

        else:
            pass
            #print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'football/sign_up.html', context)


def sign_in(request):
    error_message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/football/dashboard')
            else:
                error_message = 'حساب کاربری شما فعال نیست'
        else:
            error_message = 'نام کاربری یا رمز عبور صحیح نیست'
    
    context = {'error_message': error_message}
    return render(request, 'football/sign_in.html', context)


@login_required
def sign_out(request):
    logout(request)
    return HttpResponseRedirect('/football')


@login_required
def dashboard(request):
    profile = request.user.profile
    article_list = profile.articles.published()
    paginator = Paginator(article_list, 3)
    page_number = request.GET.get('page', 1)
    articles = paginator.get_page(page_number)
    context = {
        'profile': profile,
        'articles': articles,
    }
    return render(request, 'football/dashboard.html', context)