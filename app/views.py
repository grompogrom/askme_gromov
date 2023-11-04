from django.shortcuts import render

from app.test_data import *
from app.tools import paginate


def index(request):
    BASE['is_logged'] = False
    page_items = paginate(QUESTIONS, request)
    context = {
        'questions': page_items.object_list,
        'hot': False,
        'page': page_items,
        'base': BASE}
    return render(request, 'index.html',context)


def hot(request):
    page_items = paginate(QUESTIONS[::-1], request)
    BASE['is_logged'] = True

    context = {
        'questions': page_items.object_list,
        'hot': True,
        'page': page_items,
        'base': BASE}
    return render(request, 'index.html', context)


def tag(request, tag_name):
    result = list(filter(lambda x: tag_name.strip() in x['tags'], QUESTIONS))
    page_items = paginate(result, request)
    context = {
        'questions': page_items.object_list,
        'hot': False,
        'page': page_items,
        'tag': tag_name,
        'base': BASE
    }
    return render(request, 'tag.html', context)


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
    title = request.GET.get('title', '1')
    return render(request, 'ask.html', {'base': BASE, 'title': title})


def settings(request):
    return render(request, 'settings.html', {'base': BASE})


def login(request):
    return render(request, 'login.html', {'base': BASE})


def register(request):
    return render(request, 'register.html', {'base': BASE})
