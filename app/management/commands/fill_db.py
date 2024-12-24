import random
import os
import string
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import AnswerLike, Question, Answer, QuestionLike, Tag, Profile
from django.core.files import File


AVATAR_PATH = os.path.join('media', "avatars/image.png")


def generate_unique_username():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


class Command(BaseCommand):
    help = 'Populate the database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Scaling factor for data generation')

    def handle(self, *args, **options):

        ratio = options['ratio']

        if ratio < 10000:
            self.stdout.write(self.style.ERROR('Ratio minimum = 10 000'))
            return

        # cleaning db
        User.objects.all().delete()
        Question.objects.all().delete()
        QuestionLike.objects.all().delete()
        Answer.objects.all().delete()
        AnswerLike.objects.all().delete()
        Tag.objects.all().delete()

        # Генерация пользователей
        users = []
        for i in range(ratio):
            user = User.objects.create_user(
                username=generate_unique_username(),
                email=f'email_{i}@mail.ru',
                password='password'
            )

            # Create a profile with the default avatar
            with open(AVATAR_PATH, 'rb') as avatar_file:
                profile = Profile.objects.create(
                    user=user,
                    nickname=f'Nickname_{i}',
                    avatar=File(avatar_file, name=f'avatar_{i}.jpg')
                )
            users.append(user)

        # Генерация тегов
        tags = [Tag.objects.create(name=f'tag_{i}') for i in range(ratio)]

        # Генерация вопросов
        questions = []
        for i in range(ratio * 10):
            question = Question.objects.create(
                title=f'Question {i}',
                text='Sample question text',
                author=random.choice(users),
                likes_count=0,  # likes_count начально 0, будем обновлять позже
                answers_count=0  # answers_count начально 0, будем обновлять позже
            )

            # Присваиваем от 1 до 5 случайных тегов
            tags_cnt = random.randint(1, 5)
            question.tags.set(random.sample(tags, k=tags_cnt))

            questions.append(question)

        # Генерация ответов и лайков к ответам
        for i in range(ratio * 10):
            # Добавление ответа на вопрос случайным пользователем
            random_user = random.choice(users)
            random_question = random.choice(questions)

            answer, created = Answer.objects.get_or_create(
                question=random_question,
                author=random_user,
                text='Sample answer text',
                likes_count=0
            )

            if created:
                # Увеличиваем счетчик ответов в вопросе, если ответ добавлен
                random_question.answers_count += 1
                random_question.save()

            # Добавление лайка для ответа случайным пользователем
            random_user = random.choice(users)

            # Создаем лайк только если его еще нет для этого ответа и пользователя
            _, created = AnswerLike.objects.get_or_create(
                user=random_user,
                answer=answer,
                is_liked=True
            )

            if created:
                # Увеличиваем счетчик лайков в ответе, если лайк добавлен
                answer.likes_count += 1
                answer.save()

        # Генерация лайков для вопросов
        for i in range(ratio * 200):
            random_user = random.choice(users)
            random_question = random.choice(questions)

            # Создаем лайк только если его еще нет для этого вопроса и пользователя
            _, created = QuestionLike.objects.get_or_create(
                user=random_user,
                question=random_question,
                is_liked=True
            )

            if created:
                # Увеличиваем счетчик лайков в вопросе, если лайк добавлен
                random_question.likes_count += 1
                random_question.save()

        self.stdout.write(self.style.SUCCESS('Database populated successfully'))
