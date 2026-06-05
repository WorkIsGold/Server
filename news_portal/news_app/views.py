from datetime import datetime

from rest_framework import generics
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView
from django.http import HttpResponse, HttpResponseForbidden
from .models import News
from .forms import NewsForm, RegisterForm, UserUpdateForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .serializers import NewsSerializer

from rest_framework.permissions import IsAuthenticatedOrReadOnly

@login_required
def news_create_view(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            News.objects.create(title=request.POST.get('title'), summary=request.POST.get('summary'), content=request.POST.get('content'), author=User.objects.get(username=request.user))
            messages.success(request, 'Новость добавлена успешно')
            return render(request, 'success.html')
    else:
        form = NewsForm()
    return render(request, 'news_form.html', {'tab_number': 2, 'form': form})


class NewsUpdateView(UpdateView):
    model = News


@login_required
def news_edit_view(request, news_id):
    news = get_object_or_404(News, id=news_id)
    if news.author != request.user:
        return HttpResponseForbidden("Вы не можете редактировать эту новость")
    initial = {
        'title': news.title,
        'summary': news.summary,
        'content': news.content,
    }
    form = NewsForm(request.POST or None, initial=initial, instance=News.objects.get(pk=news_id))
    if request.method == 'POST':
        form.save()
        messages.success(request, 'Новость изменена успешно')
        return render(request, 'success.html')
    return render(request, 'news_form.html', {'form': form})


@login_required
def news_delete_view(request, news_id):
    news = get_object_or_404(News, id=news_id)
    if news.author != request.user:
        return HttpResponseForbidden("Вы не можете удалить эту новость")
    if request.method == 'POST':
        News.objects.filter(id=news_id).delete()
        messages.success(request, 'Удаление прошло успешно')
        return render(request, 'success.html')
    return render(request, 'news_confirm_delete.html')


def register_view(request):
    username = "1234567890"
    if request.method == 'POST':
        username = request.POST['first_name'] + " " + request.POST['last_name']
        if User.objects.filter(username=username).exists():
            print("Пользователь с таким именем уже существует")
        form = RegisterForm(request.POST)
        print(form.username)
        if form.is_valid():
            user = form.save()
            print('save')
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form, 'username': username})


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if request.method == 'POST':
        print("form", form)
        print(form['first_name'], form['last_name'], form['password'])
        if form.is_valid():
            username = request.POST['first_name'] + " " + request.POST['last_name']
            user = authenticate(request, username=username, password=request.POST['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
    return render(request, 'login.html', {'form': form})


@login_required
def profile_view(request):
    user = User.objects.get(username=request.user)
    initial = {
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
    form = UserUpdateForm(request.POST or None, initial=initial, instance=user)
    if request.method == 'POST':
        form.save()
        messages.success(request, 'Профиль обновлен успешно')
        print(request.POST.get('delete_button'))
        return render(request, 'success.html')
    return render(request, 'profile.html', {'form': form})


def home_view(request):
    data = {'tab_number': 1, 'news_list': News.objects.order_by('-date_updated')}
    return render(request, 'home.html', context=data)


def news_detail_view(request, news_id=0):
    news = News.objects.get(id=news_id)
    print(news.date_updated)
    data = {'news_id': news_id, 'title': news.title, 'summary': news.summary, 'content': news.content, 'date_updated': news.date_updated, 'author': news.author}
    return render(request, 'news_detail.html', context=data)


@login_required
def success_view(request):
    return render(request, 'success.html')

class NewsListCreateView(generics.ListCreateAPIView):
    """
    GET: Получить список всех новостей
    POST: Создать новую новость
    """
    queryset = News.objects.all().order_by('-date_created')
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Автоматическое назначение автора при создании новости
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class NewsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Получить конкретную новость
    PUT/PATCH: Обновить новость
    DELETE: Удалить новость
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
