from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('news/<int:news_id>/', views.news_detail_view, name='news'),
    # path('news/<int:news_id>/edit/', views.news_edit_view, name='edit'),
    path('news/<int:news_id>/edit/', views.NewsUpdateView.as_view(), name='edit'),
    path('news/<int:news_id>/delete/', views.news_delete_view, name='delete'),
    path('news/add/', views.news_create_view, name='add'),
    path('news/success/', views.success_view, name='success'),
    path('register/', views.register_view, name='register'),
    #path('login/', LoginView, name='login'),
    #path('logout/', LogoutView, name='logout'),
    #path('profile/', profile_open, name='profile'),
    #path('profile/delete/', )
]