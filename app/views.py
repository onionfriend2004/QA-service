from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike

def paginate(objects_list, request, per_page=3, adjacent_pages=2):
    page_number = request.GET.get('page', 1)
    paginator = Paginator(objects_list, per_page)
    try:
        page_items = paginator.page(page_number)
    except PageNotAnInteger:
        page_items = paginator.page(1)
        page_number = 1
    except EmptyPage:
        page_items = paginator.page(paginator.num_pages)
        page_number = paginator.num_pages

    page_number = int(page_number)

    total_pages = paginator.num_pages
    start_page = max(page_number - adjacent_pages, 1)
    end_page = min(page_number + adjacent_pages, total_pages)
    rang = list(range(start_page, end_page + 1))
    return {
        'page_items': page_items,
        'page_number': page_number,
        'total_pages': total_pages,
        'rang': rang
    }

def index(request):
    popular_users = Profile.objects.popular_users()
    popular_tags = Tag.objects.popular_tags()
    questions_page = paginate(Question.objects.all(), request)

    context = {
        'content': questions_page,
        'popular_tags': popular_tags,
        'popular_users': popular_users,
    }

    return render(request, 'index.html', context)

def ask(request):
    popular_users = Profile.objects.popular_users()
    popular_tags = Tag.objects.popular_tags()

    context = {
        'popular_tags': popular_tags,
        'popular_users': popular_users
    }

    return render(request, 'ask.html', context)

def question(request, id_question):
    popular_users = Profile.objects.popular_users()
    popular_tags = Tag.objects.popular_tags()
    question_item = Question.objects.get(id=id_question)
    answers = Answer.objects.by_question(id_question)
    content = paginate(answers, request, per_page=5)

    context = {
        'content': content,
        'question': question_item,
        'popular_tags': popular_tags,
        'popular_users': popular_users,
    }

    return render(request, 'question.html', context)


def tag(request, id_tag):
    tag = Tag.objects.get(id=id_tag)
    popular_users = Profile.objects.popular_users()
    popular_tags = Tag.objects.popular_tags()
    questions = Question.objects.by_tag(tag)
    content = paginate(questions, request)

    context = {
        'content': content,
        'tag': tag,
        'popular_tags': popular_tags,
        'popular_users': popular_users,
    }

    return render(request, 'tag.html', context)


def hot(request):
    popular_users = Profile.objects.popular_users()
    popular_tags = Tag.objects.popular_tags()
    questions = Question.objects.hot()
    content = paginate(questions, request)

    context = {
        'content': content,
        'popular_tags': popular_tags,
        'popular_users': popular_users,
    }

    return render(request, 'hot.html', context)


def login(request):
    popular_users = Profile.objects.popular_users()
    popular_tags = Tag.objects.popular_tags()

    context = {
        'popular_tags': popular_tags,
        'popular_users': popular_users
    }
    return render(request, 'login.html', context)

def signup(request):
    popular_users = Profile.objects.popular_users()
    popular_tags = Tag.objects.popular_tags()

    context = {
        'popular_tags': popular_tags,
        'popular_users': popular_users
    }
    return render(request, 'signup.html', context)

def settings(request):
    popular_users = Profile.objects.popular_users()
    popular_tags = Tag.objects.popular_tags()

    context = {
        'popular_tags': popular_tags,
        'popular_users': popular_users
    }
    return render(request, 'settings.html', context)