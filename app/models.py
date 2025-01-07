from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    nickname = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes_count = models.IntegerField(default=0)
    answers_count = models.PositiveIntegerField(default=0)

    def is_liked_by(self, user):
        return self.likes.filter(user=user, is_liked=True).exists()

    def is_disliked_by(self, user):
        return self.likes.filter(user=user, is_disliked=True).exists()
    
    # Define a custom model manager for common queries
    class QuestionManager(models.Manager):
        def new(self):
            return self.order_by('-created_at')
        
        def hot(self):
            return self.order_by('-likes_count')
        
        def by_tag(self, tag):
            return self.filter(tags__name=tag)
    
    objects = QuestionManager()


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes_count = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False)

    def is_liked_by(self, user):
        return self.likes.filter(user=user, is_liked=True).exists()

    def is_disliked_by(self, user):
        return self.likes.filter(user=user, is_disliked=True).exists()


class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    is_liked = models.BooleanField(default=False)
    is_disliked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'question')


class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    is_liked = models.BooleanField(default=False)
    is_disliked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'answer')