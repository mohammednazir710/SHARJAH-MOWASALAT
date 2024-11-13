from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def route(request):
    return render(request, 'route.html')

def schadule(request):
    return render(request, 'schadule.html')

def test(request):
    return render(request, 'test.html')