from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView
from django.http import HttpResponse, HttpResponseForbidden
from .models import News
from .forms import NewsForm, RegisterForm, UserUpdateForm, UserLoginForm
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

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
    print('-----------------edit----------------------')
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
        #news.title = request.POST.get('title')
        #news.summary = request.POST.get('summary')
        #news.content = request.POST.get('content')
        #news.save()
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
        print('-------------message---------------')
        messages.success(request, 'Удаление прошло успешно')
        print('-----------delete-----------')
        return render(request, 'success.html')
    return render(request, 'news_confirm_delete.html')

def register_view(request):
    username = "1234567890"
    if request.method == 'POST':
        print('====================================================')
        print(User.objects.all())
        username = request.POST['first_name'] + " " + request.POST['last_name']
        print('------------------', username, '--------------------')
        if User.objects.filter(username=username).exists():
            print("Пользователь с таким именем уже существует")
        form = RegisterForm(request.POST)
        #form.username = username
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
            #print(username, request.POST['password'])
            user = authenticate(request, username=username, password=request.POST['password'])
            print('------------------login---------------------')
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

        """if request.method == 'GET':
            #print('-----------------user-want-delete------------------')
            User.objects.filter(username=request.user).delete()
            messages.success(request, 'Удаление аккаунта прошло успешно')
            return render(request, 'success.html')"""
    return render(request, 'profile.html', {'form': form})

# Create your views here.
def home_view(request):
    data = {'tab_number': 1, 'news_list': News.objects.order_by('-date_updated')}
    #data = {'tab_number': 1, 'news_list': load_news()}
    return render(request, 'home.html', context=data)


def news_detail_view(request, news_id=0):
    #news = load_news(news_id)
    print('--------------------------------------------------------------------------------------')
    #print(News.objects.get(pk=news_id).title)
    news = News.objects.get(id=news_id)
    data = {'news_id': news_id, 'title': news.title, 'summary': news.summary, 'content': news.content, 'date_updated': news.date_updated, 'author': news.author}
    return render(request, 'news_detail.html', context=data)


"""def add_news_view(request):
    #CREATE NEW NEWS
    if request.method == 'POST':
        last_index = len(load_news())
        print(load_news())
        print(last_index)
        news = {'id': last_index, 'title': request.POST.get('title'), 'summary': request.POST.get('summary'), 'content': request.POST.get('content'), 'date': datetime.now().strftime("%Y-%m-%d")}
        save_news(news)
        return render(request, 'success.html')
    else:
        return render(request, 'news_form.html', {'tab_number': 2, 'form': NewsForm()})"""

@login_required
def success_view(request):
    return render(request, 'success.html')


"""#Functions for work with JSON
filename = 'news_app/data/news.json'


def load_news(news_id=-1):
    with open(filename, 'r') as json_file:
        news_list = json.load(json_file)['news']
        if news_id == -1:  #хотим получить все новости
            news_list.sort(key=lambda x: x['date'], reverse=True)
            return news_list
        if news_id < len(news_list):  #хотим получить конкретную новость
            return news_list[news_id]
    return None  #хотим то, чего нет


def save_news(news):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
        data['news'].append(news)
    with open(filename, 'w') as json_file:
        json.dump(data, json_file)"""
