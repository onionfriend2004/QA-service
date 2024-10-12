from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def ask(request):
    return render(request, 'ask.html')

def question(request, id_question):
    return render(request, 'question.html')

def tag(request, id_tag):
    return render(request, 'tag.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def settings(request):
    return render(request, 'settings.html')