from random import random
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Answer, Question

# Главная страница - список новых вопросов
def index(request):
    questions = Question.objects.new()
    page = paginate(questions, request)
    return render(request, 'index.html', {'questions': page, 'is_hot_questions': False})

# Список "популярных" вопросов
def hot_questions(request):
    questions = Question.objects.hot()
    page = paginate(questions, request)
    return render(request, 'index.html', {'questions': page, 'is_hot_questions': True})

# Список вопросов по тэгу
def questions_by_tag(request, tag):
    questions = Question.objects.filter(tags__name=tag)
    page = paginate(questions, request)
    return render(request, 'tag.html', {'questions': page, 'tag': tag})

# Страница одного вопроса с ответами
def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(question=question).order_by('-likes_count')    
    page = paginate(answers, request)
    
    return render(request, 'question.html', { 'answers': page, 'question': question })

# Форма входа
def login_view(request):
    return render(request, 'login.html')

# Форма регистрации
def signup_view(request):
    return render(request, 'register.html')

# Форма регистрации
def settings_view(request):
    return render(request, 'settings.html')

# Форма создания вопроса
def ask_question(request):
    return render(request, 'ask.html')

# пагинация
def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)

    try:
        page = paginator.page(page_number)
        page.adjusted_elided_pages = paginator.get_elided_page_range(page_number, on_each_side=2, on_ends=1)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(0)

    return page