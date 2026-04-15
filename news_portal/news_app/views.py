from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return render(request, 'home.html')
def news(request, news_id = 1):
    return HttpResponse("Hello, world.")
def add(request):
    return HttpResponse("Hello, world.")
def success(request):
    return HttpResponse("Hello, world.")
