from django.urls import path
from . import views

app_name = 'football'
urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:slug>', views.category, name='category'),
    path('article/<slug:slug>', views.article, name='article'),
    path('add-article', views.add_article, name='add-article'),
    path('sign-up', views.sign_up, name='sign-up'),
    path('sign-in', views.sign_in, name='sign-in'),
    path('sign-out', views.sign_out, name='sign-out'),
    path('dashboard', views.dashboard, name='dashboard'),
    #path('edit-user/<slug:username>', views.edit_user, name='edit-user'),
    #path('user-info/<slug:username>', views.user_info, name='user-info'),
    #path('edit-article/<slug:slug>', views.edit_article, name='edit-article'),
]