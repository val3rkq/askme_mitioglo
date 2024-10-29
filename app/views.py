from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Главная страница - список новых вопросов
def index(request):
    questions = [{"title": f"title {i}", "id": i, "text": f"text {i}"} for i in range(1, 30)]
    page = paginate(questions, request)
    return render(request, 'index.html', {'questions': page})

# Список "лучших" вопросов
def hot_questions(request):
    questions = [{"title": f"Hot title {i}", "id": i, "text": f"text {i}"} for i in range(1, 20)]
    page = paginate(questions, request)
    return render(request, 'hot.html', {'questions': page})

# Список вопросов по тэгу
def questions_by_tag(request, tag):
    questions = [{"title": f"{tag} title {i}", "id": i, "text": f"text {i}"} for i in range(1, 15)]
    page = paginate(questions, request)
    return render(request, 'tag.html', {'questions': page, 'tag': tag})

# Страница одного вопроса с ответами
def question_detail(request, question_id):
    question = {"title": f"title {question_id}", "text": f"text {question_id}", "id": question_id}
    answers = [{"text": f"answer {i}"} for i in range(1, 5)]
    return render(request, 'question.html', {'question': question, 'answers': answers})

# Форма входа
def login_view(request):
    return render(request, 'login.html')

# Форма регистрации
def signup_view(request):
    return render(request, 'register.html')

# Форма создания вопроса
def ask_question(request):
    return render(request, 'ask.html')

def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page