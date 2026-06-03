from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('news/<int:news_id>/', views.news_detail_view, name='news'),
    #path('news/<int:news_id>/edit/', views.news_edit_view, name='edit'),
    path('news/<int:news_id>/edit/', views.news_edit_view, name='edit'),
    path('news/<int:news_id>/delete/', views.news_delete_view, name='delete'),
    path('news/add/', views.news_create_view, name='add'),
    path('news/success/', views.success_view, name='success'),
    path('register/', views.register_view, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    #path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    #path('profile/delete/', )
    'talk.views',
    url(r'^$', 'home'),
    url(r'^api/v1/posts/$', 'post_collection'),
    url(r'^api/v1/posts/(?P<pk>[0-9]+)$', 'post_element'),
]