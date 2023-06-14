from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Person(models.Model):
    name = models.CharField(max_length=30)
    age = models.SmallIntegerField()
    email = models.EmailField()

    def __str__(self):
        return '{}, {} years old.'.format(self.name, self.age)
    
class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question')
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return '{} - Question: {}'.format(self.user, self.title[:20])

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer')
    Question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - Answer to: {}'.format(self.user, self.Question.title[:20])