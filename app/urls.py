from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('hot/', views.hot_questions, name='hot_questions'),  # Список "лучших" вопросов
    path('tag/<str:tag>/', views.questions_by_tag, name='questions_by_tag'),  # Вопросы по тэгу
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),  # Один вопрос
    path('login/', views.login_view, name='login'),  # Форма входа
    path('signup/', views.signup_view, name='signup'),  # Форма регистрации
    path('settings/', views.settings_view, name='settings'),  # Форма настроек
    path('ask/', views.ask_question, name='ask_question'),  # Создание вопроса
]