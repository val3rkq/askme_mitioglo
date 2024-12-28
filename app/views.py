from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import Answer, Question, Tag, Profile

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
    questions = Question.objects.by_tag(tag)
    page = paginate(questions, request)
    return render(request, 'tag.html', {'questions': page, 'tag': tag})


# Страница одного вопроса с ответами
@login_required
def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(question=question).order_by('-likes_count', '-created_at')
    page = paginate(answers, request)

    form = AnswerForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            text = form.cleaned_data['text']
            Answer.objects.create(
                question=question,
                author=request.user,
                text=text
            )

            # Увеличиваем счетчик ответов в модели Question
            question.answers_count += 1
            question.save()

            return redirect('question', question_id=question.id)
        else:
            messages.error(request, 'Ошибка при создании ответа!')
    else:
        form = AnswerForm()

    return render(request, 'question.html', {
        'answers': page,
        'question': question,
        'form': form
    })


# Форма входа
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    login_form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if login_form.is_valid():
            login_field = login_form.cleaned_data["login"]
            password = login_form.cleaned_data["password"]
            user = authenticate(request, username=login_field, password=password)
            if user is not None:
                login(request, user)
                continue_url = request.GET.get('continue', '/')
                return redirect(continue_url)
            else:
                messages.error(request, 'Неверный логин или пароль!')
        else:
            messages.error(request, 'Что-то пошло не так!')

    return render(request, 'login.html', {'form': login_form})


# Форма регистрации
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    signup_form = SignUpForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if signup_form.is_valid():
            try:
                if User.objects.filter(username=signup_form.cleaned_data['login']).exists():
                    messages.error(request, 'Пользователь с таким логином уже существует!')
                else:
                    user = signup_form.create_user()
                    
                    profile = Profile(user=user, 
                                    nickname = signup_form.cleaned_data['nickname'])
                    # profile.avatar=signup_form.cleaned_data.get('avatar', None), 
                    profile.save()
                    
                    login_field = signup_form.cleaned_data["login"]
                    password = signup_form.cleaned_data["password"]
                    user = authenticate(request, username=login_field, password=password)
                    if user is not None:
                        login(request, user)
                        continue_url = request.GET.get('continue', '/')
                        return redirect(continue_url)
                    else:
                        messages.error(request, 'Ошибка аутентификации после регистрации!')
            except Exception as e:
                messages.error(request, f'Ошибка при создании пользователя! {e}')
        else:
            messages.error(request, 'Проверьте правильность введенных данных!')

    return render(request, 'register.html', {'form': signup_form})


# форма выхода
@login_required(redirect_field_name='continue')
def logout_view(request):
    logout(request)
    return redirect('index')


# Форма редактирования профиля
@login_required(redirect_field_name='continue')
def settings_view(request):
    user = request.user
    
    # Проверяем, существует ли профиль у пользователя
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Обновление данных пользователя
                user.username = form.cleaned_data['login']
                user.email = form.cleaned_data['email']
                user.save()

                # Обновление данных профиля
                profile.nickname = form.cleaned_data['nickname']
                # if 'avatar' in request.FILES:
                #     profile.avatar = request.FILES['avatar']
                profile.save()

                return redirect('settings')
            except Exception as e:
                messages.error(request, 'Ошибка при обновлении настроек!')
        else:
            messages.error(request, 'Проверьте правильность введенных данных.')
    else:
        form = SettingsForm(initial={
            'login': user.username,
            'email': user.email,
            'nickname': profile.nickname,
        })

    return render(request, 'settings.html', {'form': form})


@login_required(redirect_field_name='continue')
def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            try:
                # Создание вопроса
                question = Question.objects.create(
                    title=form.cleaned_data['title'],
                    text=form.cleaned_data['text'],
                    author=request.user
                )
                
                # Обработка тегов
                tags = form.cleaned_data['tags'].split(',')
                for tag_name in tags:
                    tag_name = tag_name.strip()  # Убираем лишние пробелы
                    if tag_name:
                        tag, created = Tag.objects.get_or_create(name=tag_name)
                        question.tags.add(tag)
                question.save()

                return redirect('question', question_id=question.id)
            except Exception as e:
                messages.error(request, 'Ошибка при создании вопроса!')
        else:
            messages.error(request, 'Проверьте правильность введенных данных.')
    else:
        form = QuestionForm()

    return render(request, 'ask.html', {'form': form})


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