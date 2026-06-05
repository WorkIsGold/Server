from django.urls import path, include
from django.contrib.auth import views as auth_views
from drf_spectacular.management.commands import spectacular
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from rest_framework.authtoken.views import obtain_auth_token

from . import views
from .views import NewsDetailView, NewsListCreateView
from .api_urls import router

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
    #path('api/v1/news/', NewsListCreateView.as_view(), name='news-list'),
    #path('api/v1/news/<int:news_id>/', NewsDetailView.as_view(), name='news-detail'),
    #path('api/users/', ),
    path('api/v1/api-token-auth', obtain_auth_token, name='api-token-auth'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('', include(router.urls)),
    #path('/api-register/', name='api-register'),
    #path('api/login/', name='api-login'),
    #path('api/logout/', name='api-logout'),
    #path('api/profile/', name='api-profile'),

    #patterns('talk.views', url(r'^$', 'home'), url(r'^api/v1/posts/$', 'post_collection'), url(r'^api/v1/posts/(?P<pk>[0-9]+)$', 'post_element')),

]