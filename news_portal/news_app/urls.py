from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('news/<int:news_id>/', views.new, name='new'),
    path('news/add', views.add, name='add'),
    path('news/success', views.success, name='success'),
]