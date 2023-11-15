import uuid

from django.contrib.auth.models import User
from django.db import models

from app.managers import QuestionManager, AnswerManager, LikeManager, TagManager


class Tag(models.Model):
    objects = TagManager()
    name = models.CharField(max_length=20, unique=True)

    def as_dict(self):
        return {'id': self.id,
                'name': self.name}


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='photos/%Y/%m/%d', null=True, blank=True)


class Question(models.Model):
    objects = QuestionManager()

    author = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    likes_count = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag)

    def get_answers_count(self):
        return Answer.objects.count_by_question(self.id)

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'likes': self.likes_count,
            'content': self.text,
            'answers': self.get_answers_count(),
            'tags': list(map(lambda x: x.as_dict(), list(self.tags.all()))),
        }


class Answer(models.Model):
    objects = AnswerManager()
    author = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    likes_count = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False)
    text = models.TextField(max_length=500)


class Like(models.Model):
    objects = LikeManager()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True, default=None)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True, default=None)


class BestProfile(models.Model):
    updated = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


class PopularTag(models.Model):
    updated = models.DateTimeField(auto_now_add=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
