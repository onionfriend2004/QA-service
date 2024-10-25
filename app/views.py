from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#заглушка
questions = [
    {
        'title': f'title {i}',
        'id': i,
        'text': f'This is text for question {i}'
    } for i in range(1, 50)
]

answers = [
    {
        'nickname': f'nickname {i}',
        'text': f'This is text for answer {i}'
    } for i in range(1, 10)
]

def paginate(objects_list, request, per_page=3, adjacent_pages=2):
    page_number = int(request.GET.get('page', 1))
    paginator = Paginator(objects_list, per_page)
    try:
        page_items = paginator.page(page_number)
    except PageNotAnInteger:
        page_items = paginator.page(1)
        page_number = 1
    except EmptyPage:
        page_items = paginator.page(paginator.num_pages)
        page_number = paginator.num_pages
    total_pages = paginator.num_pages
    start_page = max(page_number - adjacent_pages, 1)
    end_page = min(page_number + adjacent_pages, total_pages)
    rang = list(range(start_page, end_page + 1))
    return (page_items, page_number, total_pages, rang)

def index(request):
    page_items, page_number, total_pages, rang = paginate(questions, request)
    return render(request, 'index.html', {
        'questions': page_items.object_list,
        'page_items': page_items,
        'page_number': page_number,
        'total_pages': total_pages,
        'rang': rang
    })

def ask(request):
    return render(request, 'ask.html')

def question(request, id_question):
    question_item = questions[id_question - 1]
    page_items, page_number, total_pages, rang = paginate(answers, request, per_page=5)
    return render(request, 'question.html', {
        'question': question_item,
        'answers': page_items.object_list,
        'page_items': page_items,
        'page_number': page_number,
        'total_pages': total_pages,
        'rang': rang
    })

def tag(request, id_tag):
    page_items, page_number, total_pages, rang = paginate(questions, request)
    return render(request, 'tag.html', {
        'questions': page_items.object_list,
        'page_items': page_items,
        'page_number': page_number,
        'total_pages': total_pages,
        'rang': rang
    })

def hot(request):
    page_items, page_number, total_pages, rang = paginate(questions, request)
    return render(request, 'hot.html', {
        'questions': page_items.object_list,
        'page_items': page_items,
        'page_number': page_number,
        'total_pages': total_pages,
        'rang': rang
    })

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def settings(request):
    return render(request, 'settings.html')