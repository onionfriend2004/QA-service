from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse

from django.contrib.postgres.search import SearchQuery, SearchRank
from django.db.models import Q, F

from app.models import *
from app.forms import *
from app.utils import get_centrifugo_info

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

def get_page_for_new_answer(answers, new_answer, per_page=5):
    answers_list = list(answers)
    position = answers_list.index(new_answer)
    page_number = (position // per_page) + 1
    
    return page_number

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

@login_required
def ask(request):
    popular_users = Profile.objects.popular_users()
    popular_tags = Tag.objects.popular_tags()

    if request.method == 'GET':
        form = QuestionForm()
    else:
        form = QuestionForm(request.user.profile, data=request.POST)
        if form.is_valid():
            question = form.save()
            return redirect(reverse('app:question', kwargs={'question_id': question.id}))

    context = {
        'form': form,
        'popular_tags': popular_tags,
        'popular_users': popular_users
    }

    return render(request, 'ask.html', context)

def question(request, question_id):
    answers = Answer.objects.by_question(question_id)
    popular_users = Profile.objects.popular_users()
    popular_tags = Tag.objects.popular_tags()
    question_item = Question.objects.get(id=question_id)
    content = paginate(answers, request, per_page=5)

    if request.method == 'GET':
        form = AnswerForm()
    else:
        if not request.user.is_authenticated:
            return redirect(f"/login/?continue={request.get_full_path()}")
        form = AnswerForm(profile_id=request.user.profile, question_id=question_item, data=request.POST)
        if form.is_valid():
            answer = form.save()
            content = paginate(answers, request, per_page=5)
            page_number = get_page_for_new_answer(answers, answer)
            return redirect(reverse('app:question', kwargs={'question_id': question_id}) + f"?page={page_number}#answer-{answer.id}")

    context = {
        'form': form,
        'content': content,
        'question': question_item,
        'popular_tags': popular_tags,
        'popular_users': popular_users,
        **get_centrifugo_info()
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

    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user is not None:
                auth_login(request, user)
                return redirect(request.POST.get('continue', reverse('app:index')))
            else:
                form.add_error(None, 'Invalid login or password')

    context = {
        'form': form,
        'popular_tags': popular_tags,
        'popular_users': popular_users
    }
    return render(request, 'login.html', context)

def logout(request):
    auth_logout(request)
    previous_page = request.META.get('HTTP_REFERER')
    if previous_page is not None:
        return redirect(previous_page)
    return redirect(reverse('app:index'))

def signup(request):
    popular_users = Profile.objects.popular_users()
    popular_tags = Tag.objects.popular_tags()

    if request.method == 'GET':
        form = SignUpForm()
    else:
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect(reverse('app:index'))

    context = {
        'form': form,
        'popular_tags': popular_tags,
        'popular_users': popular_users
    }
    return render(request, 'signup.html', context)

@login_required
def settings(request):
    popular_users = Profile.objects.popular_users()
    popular_tags = Tag.objects.popular_tags()

    form_updated = False

    if request.method == 'GET':
        form = SettingsForm(user=request.user, instance=request.user)
        avatar = ImageForm(instance=request.user.profile)
        form_updated = request.GET.get('updated') == 'true'
    else:
        form = SettingsForm(data=request.POST, user=request.user, instance=request.user)
        avatar = ImageForm(data=request.POST, files=request.FILES, instance=request.user.profile)

        if form.is_valid() and avatar.is_valid():
            user = form.save()
            avatar.save()
            form_updated = True
            auth_login(request, user)
            return redirect(reverse('app:settings') + '?updated=true')

    context = {
        'form': form,
        'avatar': avatar,
        'form_updated': form_updated,
        'popular_tags': popular_tags,
        'popular_users': popular_users
    }
    return render(request, 'settings.html', context)

@require_POST
@login_required
def like(request):
    data = request.POST
    rating = 0
    if data['type'] == 'question':
        form = QuestionLikeForm(user=request.user.profile, question=data['id'], is_like=(data['action'] == 'like'))
        rating = form.save()
    elif data['type'] == 'answer':
        form = AnswerLikeForm(user=request.user.profile, answer=data['id'], is_like=(data['action'] == 'like'))
        rating = form.save()

    return JsonResponse({'rating': rating})

@require_POST
@login_required
def is_correct(request):
    data = request.POST
    answer = Answer.objects.get(pk=data['id'])
    if Answer.objects.filter(question_id=answer.question_id, is_correct=True).count() < 3 or answer.is_correct:
        answer.change_mind_correct()
    return JsonResponse({'action': answer.is_correct})

@require_POST
def search(request):
    q = request.POST.get('query', '')
    if q:
        q = ' '.join(q.split())
    query = SearchQuery(q)
    queryset = Question.objects.annotate(
        rank=SearchRank(F('search'), query)
    ).filter(Q(rank__gte=0.03)).order_by('-rank')

    results = [{'title': question.title, 'url': reverse('app:question', kwargs={'question_id': question.id})} for question in queryset]
    print(results)
    return JsonResponse({'results': results})