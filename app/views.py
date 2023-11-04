from django.core.paginator import Paginator
from django.shortcuts import render

from app.tools import paginate

# Create your views here.
QUESTIONS = [{
        'id': i,
        'title': f'Question {i}',
        'likes': i * 2 + 1,
        'answers': i,
        'content': f'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor',
        'tags': [f'tag {i} 1', f'tag {i} 3', f'tag {i} 2']
    } for i in range(100)]

IS_LOGGED = True
BEST_MEMBERS = ['Maslove', 'Brin', 'Page', 'Musk']
POPULAR_TAGS = [{
    'id': i,
    'name': f'name {i}'
} for i in range(10)]
BASE = {
    'is_logged': IS_LOGGED,
    'best_members': BEST_MEMBERS,
    'popular_tags': POPULAR_TAGS}


def index(request):
    page_items = paginate(QUESTIONS, request)
    context = {
        'questions': page_items.object_list,
        'hot': False,
        'page': page_items,
        'base': BASE}
    return render(request, 'index.html',context)


def hot(request):
    page_items = paginate(QUESTIONS[::-1], request)
    context = {
        'questions': page_items.object_list,
        'hot': True,
        'page': page_items,
        'base': BASE}
    return render(request, 'index.html', context)


def question(request, question_id):
    item = QUESTIONS[question_id]
    answers = [{
        'author': f'author {i}',
        'content': f'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore',
        'likes_count': i * 2
    } for i in range(100)]
    page_items = paginate(answers, request, 5)
    context = {
        'question': item,
        'answers': page_items.object_list,
        'page': page_items,
        'base': BASE}
    return render(request, 'question.html', context)


def ask(request):

    return render(request, 'ask.html', {'base': BASE})


def settings(request):
    return render(request, 'settings.html', {'base': BASE})


def login(request):
    return render(request, 'login.html', {'base': BASE})


def register(request):
    return render(request, 'register.html', {'base': BASE})
