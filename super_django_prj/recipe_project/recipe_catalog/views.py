from django.http import HttpResponse
from django.shortcuts import render


def about(request):
    return HttpResponse("О проекте")


def index(request):
    return HttpResponse('Главная страница')


def recipe_detail(request, pk):
    return HttpResponse(f'Описание проекта id = {pk}')
