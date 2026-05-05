from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from .forms import NewsForm
import json

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

@login_required
def news_create_view(request):
    if request.method == 'POST':
        news = News.objects.create(title=request.POST.get('title'), summary=request.POST.get('summary'), content=request.POST.get('content'), author=User.objects.get(username=request.user))
        return render(request, 'success.html')
    else:
        return render(request, 'add_news.html', {'tab_number': 2, 'form': NewsForm()})

def news_edit_view(request, news_id):
    news = get_object_or_404(News, id=news_id)
    if news.author != request.user:
        return HttpResponseForbidden("Вы не можете редактировать эту новость")
    if request.method == 'POST':
        if request.POST.get('title') != '':
            news.title = request.POST.get('title')
        if request.POST.get('summary') != '':
            news.summary = request.POST.get('summary')
        if request.POST.get('content') != '':
            news.content = request.POST.get('content')
        news.save()
        return render(request, 'success.html')
    return render(request, 'home.html')

def news_delete_view(request, news_id):
    news = get_object_or_404(News, id=news_id)
    if news.author != request.user:
        return HttpResponseForbidden("Вы не можете удалить эту новость")
    News.objects.filter(id=news_id).delete()
    return render(request, 'success.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


# Create your views here.
def home_view(request):
    data = {'tab_number': 1, 'news_list': load_news()}
    return render(request, 'home.html', context=data)


def news_detail_view(request, news_id=1):
    news = load_news(news_id)
    data = {'title': news['title'], 'summary': news['summary'], 'content': news['content'], 'date': news['date']}
    return render(request, 'news_detail.html', context=data)


def add_news_view(request):
    #CREATE NEW NEWS
    if request.method == 'POST':
        last_index = len(load_news())
        print(load_news())
        print(last_index)
        news = {'id': last_index, 'title': request.POST.get('title'), 'summary': request.POST.get('summary'), 'content': request.POST.get('content'), 'date': datetime.now().strftime("%Y-%m-%d")}
        save_news(news)
        return render(request, 'success.html')
    else:
        return render(request, 'add_news.html', {'tab_number': 2, 'form': NewsForm()})


def success_view(request):
    return render(request, 'success.html')


#Functions for work with JSON
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
        json.dump(data, json_file)
