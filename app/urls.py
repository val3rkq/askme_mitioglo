from django.urls import path
from . import views
from askme import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('hot/', views.hot_questions, name='hot'),  # Список "лучших" вопросов
    path('tag/<str:tag>/', views.questions_by_tag, name='tag'),  # Вопросы по тэгу
    path('question/<int:question_id>/', views.question_detail, name='question'),  # Один вопрос
    path('login/', views.login_view, name='login'),  # Форма входа
    path('signup/', views.signup_view, name='signup'),  # Форма регистрации
    path('settings/', views.settings_view, name='settings'),  # Форма настроек
    path('ask/', views.ask_question, name='ask'),  # Создание вопроса
    path('logout/', views.logout_view, name='logout'),  # Выход
    path('like_question/', views.like_question, name='like_question'),  # Лайк вопроса
    path('like_answer/', views.like_answer, name='like_answer'),  # Лайк ответа
    path('mark_correct_answer/', views.mark_correct_answer, name='mark_correct_answer'),  # Проверка ответа
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)