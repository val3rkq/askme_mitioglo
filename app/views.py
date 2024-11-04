from random import random
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

questions = [
    {
        "title": f"title {i}", 
        "id": i, 
        "text": f"text {i}",
        "likes": 100 - i,
        "answers_cnt": i % 7,
        "tags": ["tag1", "tag2", "tag3"],
    } for i in range(1, 30)
]

# Главная страница - список новых вопросов
def index(request):
    page = paginate(questions, request)
    return render(request, 'index.html', {'questions': page, 'is_hot_questions': False})

# Список "лучших" вопросов
def hot_questions(request):
    hot_questions_list = questions[:15]
    page = paginate(hot_questions_list, request)
    return render(request, 'index.html', {'questions': page, 'is_hot_questions': True})

# Список вопросов по тэгу
def questions_by_tag(request, tag):
    questions_list = list(filter(lambda question: tag in question["tags"], questions))
    page = paginate(questions_list, request)
    return render(request, 'tag.html', {'questions': page, 'tag': tag})

# Страница одного вопроса с ответами
def question_detail(request, question_id):
    answers = [{"text": f"answer {i} text ... {i}", "likes": i % 3} for i in range(questions[question_id - 1]["answers_cnt"])]
    page = paginate(answers, request)
    return render(request, 'question.html', {'answers': page, 'question': questions[question_id - 1]})

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

def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page