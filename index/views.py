from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages


def index(request):
    context = {

    }
    return render(request, 'index.html', context=context)
