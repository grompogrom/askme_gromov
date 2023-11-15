from django.http import HttpResponseNotFound
from django.shortcuts import render

from app.models import Question, Tag, Answer
from app.tools import paginate, get_base


def index(request):
    questions = Question.objects.all_new()
    page_items = paginate(questions, request)
    context = {
        'questions': page_items.object_list,
        'hot': False,
        'page': page_items,
        'base': get_base()}
    return render(request, 'index.html', context)


def hot(request):
    questions = Question.objects.all_hot()
    page_items = paginate(questions, request)
    context = {
        'questions': page_items.object_list,
        'hot': True,
        'page': page_items,
        'base': get_base()}
    return render(request, 'index.html', context)


def tag(request, tag_name):
    try:
        tag = Tag.objects.get(name=tag_name)
        result = tag.question_set.all()
    except Tag.DoesNotExist:
        return HttpResponseNotFound()

    page_items = paginate(result, request)
    context = {
        'questions': page_items.object_list,
        'page': page_items,
        'tag': tag_name,
        'base': get_base()
    }
    return render(request, 'tag.html', context)


def question(request, question_id):
    try:
        item = Question.objects.get(id=question_id)
        answers = Answer.objects.filter(question=question_id)
    except Question.DoesNotExist:
        return HttpResponseNotFound()

    page_items = paginate(answers, request, 5)
    context = {
        'question': item.as_dict(),
        'answers': page_items.object_list,
        'page': page_items,
        'base': get_base()}
    return render(request, 'question.html', context)


def ask(request):
    title = request.GET.get('title', '1')
    return render(request, 'ask.html', {'base': get_base(), 'title': title})


def settings(request):
    return render(request, 'settings.html', {'base': get_base()})


def login(request):
    return render(request, 'login.html', {'base': get_base()})


def register(request):
    return render(request, 'register.html', {'base': get_base()})
