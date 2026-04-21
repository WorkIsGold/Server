from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from .forms import NewsForm
import json


# Create your views here.
def home_view(request):
    data = {'tab_number': 1, 'news_list': load_news()}
    return render(request, 'home.html', context=data)


def news_detail_view(request, news_id=1):
    news = load_news(news_id)
    data = {'title': news['title'], 'summary': news['summary'], 'content': news['content']}
    return render(request, 'news_detail.html', context=data)


def add_news_view(request):
    #CREATE NEW NEWS
    if request.method == 'POST':
        last_index = len(load_news())
        print(load_news())
        print(last_index)
        news = {'id': last_index, 'title': request.POST.get('title'), 'summary': request.POST.get('summary'), 'content': request.POST.get('content'), 'date:': datetime.now().strftime("%Y-%m-%d")}
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
