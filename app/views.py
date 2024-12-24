from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .forms import *
from .models import Answer, Question, Tag, Profile, QuestionLike, AnswerLike

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
    answers = Answer.objects.filter(question=question).order_by('-created_at')

    for answer in answers:
        like_obj = AnswerLike.objects.filter(user=request.user, answer=answer).first()
        
        if like_obj:
            answer.is_liked = like_obj.is_like
            answer.is_disliked = like_obj.is_dislike
        else:
            answer.is_liked = False
            answer.is_disliked = False

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
                user = signup_form.create_user()
                profile = Profile(user=user, 
                                  avatar=signup_form.cleaned_data.get('avatar', None), 
                                  nickname = signup_form.cleaned_data['nickname'])
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
                messages.error(request, f'Ошибка при создании пользователя: {str(e)}')
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

                profile.nickname = form.cleaned_data['nickname']                
                # Обновление данных профиля
                if form.cleaned_data['avatar'] is not None:
                    profile.avatar = form.cleaned_data.get('avatar', profile.avatar)
                
                profile.save()

                return redirect('settings')
            except Exception as e:
                messages.error(request, f'Ошибка при обновлении настроек: {e}')
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
                messages.error(request, f'Ошибка при создании вопроса: {e}')
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


@login_required(login_url="login")
@csrf_exempt
def like_question(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        action = request.POST.get('action')  # "like" или "dislike"

        if not question_id or not action:
            return JsonResponse({'error': 'Missing parameters'}, status=400)

        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return JsonResponse({'error': 'Question not found'}, status=404)

        user = request.user
        like_obj, created = QuestionLike.objects.get_or_create(user=user, question=question)

        if action == 'like':
            # Проверяем, не добавлялся ли уже лайк
            if not created:
                return JsonResponse({'error': 'Already liked'}, status=400)
        elif action == 'dislike':
            # Удаляем лайк, если он был
            like_obj.delete()
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)

        # Пересчитываем количество лайков
        question.likes_count = question.likes.count()
        question.save()

        return JsonResponse({'new_rating': question.likes_count}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
@login_required
def like_answer(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    answer_id = request.POST.get('answer_id')
    action = request.POST.get('action')  # "like" or "dislike"

    if not answer_id or not action:
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    try:
        answer = Answer.objects.get(id=answer_id)
    except Answer.DoesNotExist:
        return JsonResponse({'error': 'Answer not found'}, status=404)

    user = request.user
    like_obj, created = AnswerLike.objects.get_or_create(user=user, answer=answer)

    if not like_obj.is_like and not like_obj.is_dislike:
        if action == 'like':
            like_obj.is_like = True
            like_obj.is_dislike = False
        elif action == 'dislike':
            like_obj.is_like = False
            like_obj.is_dislike = True

    elif like_obj.is_like and not like_obj.is_dislike:
        if action == 'like':
            like_obj.is_like = False
            like_obj.is_dislike = False
        elif action == 'dislike':
            like_obj.is_like = False
            like_obj.is_dislike = True
    
    elif not like_obj.is_like and like_obj.is_dislike:
        if action == 'like':
            like_obj.is_like = True
            like_obj.is_dislike = False
        elif action == 'dislike':
            like_obj.is_like = False
            like_obj.is_dislike = False

    else:
        return JsonResponse({'error': 'Invalid action'}, status=400)

    like_obj.save()
    likes_count = answer.likes.filter(is_like=True).count()
    dislikes_count = answer.likes.filter(is_dislike=True).count()
    answer.likes_count = likes_count - dislikes_count
    answer.save()

    return JsonResponse({'new_rating': answer.likes_count}, status=200)


@csrf_exempt
@login_required
def mark_correct_answer(request):
    if request.method == 'POST':
        answer_id = request.POST.get('answer_id')
        question_id = request.POST.get('question_id')
        is_correct = request.POST.get('is_correct') == 'true'

        try:
            answer = Answer.objects.get(id=answer_id)
            question = Question.objects.get(id=question_id)

            # Проверка, что только автор вопроса может изменять правильный ответ
            if question.author != request.user:
                return JsonResponse({'status': 'error', 'message': 'Вы не автор вопроса!'}, status=403)

            answer.is_correct = is_correct
            answer.save()

            return JsonResponse({'status': 'success'}, status=200)

        except (Answer.DoesNotExist, Question.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'Неверный ответ или вопрос!'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method!'}, status=405)