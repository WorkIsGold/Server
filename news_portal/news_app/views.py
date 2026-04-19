from django.shortcuts import render
from django.http import HttpResponse
import json
# Create your views here.
def home_view(request):
    return render(request, 'home.html')
def news_detail_view(request, news_id = 1):
    news_list = load_news(news_id)
    return render(request, 'news_detail.html')
def add_news_view(request):
    #CREATE NEW NEWS
    if request.method == 'POST':
        last_index = len(load_news())
        print(load_news())
        print(last_index)
        news = {'id': last_index, 'subtext': request.POST.get('subtext'), 'text': request.POST.get('text')}
        save_news(news)
    return render(request, 'add_news.html')
def success_view(request):
    return render(request, 'success.html')
#Functions for work with JSON
def load_news(news_id = -1):
    news_list = json.load(open('news.json'))['news']
    if news_id == -1: #хотим получить все новости
        return news_list
    if news_id < len(news_list): #хотим получить конкретную новость
        return news_list[news_id]
    return None #хотим то, чего нет

def save_news(news):
    with open('news.json', 'r') as json_file:
        data = json.load(json_file)
        data['news'].append(news)
    with open('news.json', 'w') as json_file:
        json.dump(data, json_file)