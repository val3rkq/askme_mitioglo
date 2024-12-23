from django.contrib import admin
from app.models import *

# Register your models here.
admin.site.register(Question)
admin.site.register(QuestionLike)
admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Answer)
admin.site.register(AnswerLike)