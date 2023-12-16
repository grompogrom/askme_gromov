from urllib.parse import urlencode

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from app.forms import LoginForm, RegisterForm, ProfileForm, QuestionForm, AnswerForm
from app.models import Question, Tag, Answer
from app.tools import paginate, get_base


def index(request):

    questions = Question.objects.all_new()
    page_items = paginate(questions, request)
    context = {
        'questions': page_items.object_list,
        'hot': False,
        'page': page_items,
        'base': get_base(request)}
    return render(request, 'index.html', context)


def hot(request):
    questions = Question.objects.all_hot()
    page_items = paginate(questions, request)
    context = {
        'questions': page_items.object_list,
        'hot': True,
        'page': page_items,
        'base': get_base(request)}
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
        'base': get_base(request)
    }
    return render(request, 'tag.html', context)


def question(request, question_id):
    try:
        item = Question.objects.get(id=question_id)
        answers = Answer.objects.filter(question=question_id)
    except Question.DoesNotExist:
        return HttpResponseNotFound()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = AnswerForm(request.user, question_id,request.POST)
        if form.is_valid():
            answer = form
            answer.save()

            url = reverse('question', args=(question_id,))
            query_string = urlencode({'page': 'last'})
            return HttpResponseRedirect(url + '?' + query_string + '#bottom')
    else:
        form = AnswerForm(request.user,question_id)

    page_items = paginate(answers, request, 5)
    context = {
        'question': item.as_dict(),
        'answers': page_items.object_list,
        'page': page_items,
        'form': form,
        'base': get_base(request)}
    return render(request, 'question.html', context)


@login_required(login_url='login', redirect_field_name='continue')
def ask(request):

    if request.method == 'POST':
        form = QuestionForm(request.user, request.POST)
        if form.is_valid():
            question = form.save()
            return redirect(reverse('question', args=(question.id,)))
    else:
        form = QuestionForm(request.user)

    return render(request, 'ask.html', {'base': get_base(request), 'form': form})


@login_required(login_url='login', redirect_field_name='continue')
def settings(request):
    if request.method == 'POST':
        form = ProfileForm(request.user, request.POST, request.FILES)
        if form.is_valid():
             form.save()
    else:
        form = ProfileForm(user=request.user)
    return render(request, 'settings.html', {'base': get_base(request), 'form': form})


def signin(request):

    # fixme extract
    if request.method == 'POST':
        origin_url = request.GET.get('continue', 'index')
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            if user is not None:
                login(request, user)
                return redirect(origin_url)
            else:
                login_form.add_error(None, 'Wrong login or password')

    elif request.method == 'GET':
        login_form = LoginForm()
    return render(request, 'login.html', {'base': get_base(request), 'form': login_form})


def register(request):
    if request.method == 'GET':
        register_form = RegisterForm()
    elif request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            if user:
                login(request, user)
                return redirect(reverse('index'))
            else:
                register_form.add_error(None, 'User saving error!')
    return render(request, 'register.html', {
        'base': get_base(request),
        'form': register_form
    })


def log_out(request):
    origin_url = request.GET.get('continue', 'index')
    logout(request)
    return redirect(origin_url)
