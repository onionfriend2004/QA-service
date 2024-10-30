from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#заглушка
tags = [
    {
        'id': i, 
        'name': f'tag{i}'
    } for i in range(1, 11)
]

questions = [
    {
        'title': f'title {i}',
        'id': i,
        'text': f'This is text for question {i}',
        'tags': [tags[i % len(tags)], tags[(i + 1) % len(tags)]]
    } for i in range(1, 50)
]

answers = [
    {
        'username': f'username {i}',
        'text': f'This is text for answer {i}'
    } for i in range(1, 10)
]

users = [
    {
        'username': f'user{i}',
    } for i in range(1, 6)
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
    popular_users = users
    popular_tags = tags
    answer_count = len(answers)
    page_items, page_number, total_pages, rang = paginate(questions, request)
    return render(request, 'index.html', {
        'questions': page_items.object_list,
        'page_items': page_items,
        'page_number': page_number,
        'total_pages': total_pages,
        'rang': rang,
        'popular_tags': popular_tags,
        'popular_users': popular_users,
        'answer_count': answer_count
    })

def ask(request):
    popular_users = users
    popular_tags = tags
    return render(request, 'ask.html', {
        'popular_tags': popular_tags,
        'popular_users': popular_users
    })

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
    tag = tags[int(id_tag) - 1]
    popular_users = users
    popular_tags = tags
    answer_count = len(answers)
    page_items, page_number, total_pages, rang = paginate(questions, request)
    return render(request, 'tag.html', {
        'questions': page_items.object_list,
        'page_items': page_items,
        'page_number': page_number,
        'total_pages': total_pages,
        'tag': tag,
        'rang': rang,
        'popular_tags': popular_tags,
        'popular_users': popular_users,
        'answer_count': answer_count
    })

def hot(request):
    popular_users = users
    popular_tags = tags
    answer_count = len(answers)
    page_items, page_number, total_pages, rang = paginate(questions, request)
    return render(request, 'hot.html', {
        'questions': page_items.object_list,
        'page_items': page_items,
        'page_number': page_number,
        'total_pages': total_pages,
        'rang': rang,
        'popular_tags': popular_tags,
        'popular_users': popular_users,
        'answer_count': answer_count
    })

def login(request):
    popular_users = users
    popular_tags = tags
    return render(request, 'login.html', {
        'popular_tags': popular_tags,
        'popular_users': popular_users
    })

def signup(request):
    popular_users = users
    popular_tags = tags
    return render(request, 'signup.html', {
        'popular_tags': popular_tags,
        'popular_users': popular_users
    })

def settings(request):
    popular_users = users
    popular_tags = tags
    return render(request, 'settings.html', {
        'popular_tags': popular_tags,
        'popular_users': popular_users
    })