from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class QuizAppUser(AbstractUser):
    profile_image = models.ImageField(upload_to='media/',default='')


class Category(models.Model):
    name = models.CharField(max_length=30,blank=False,null=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None, null=True)
    question = models.CharField(max_length=255)

    def __str__(self):
        return self.question


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=50)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer


class Quiz(models.Model):
    owner = models.ForeignKey(QuizAppUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    score = models.CharField(max_length=10, null=True)


class Guess(models.Model):
    submitted_by = models.ForeignKey(QuizAppUser, on_delete=models.CASCADE)
    answered_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_given = models.ForeignKey(Choice, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)


class Update(models.Model):
    first_name=models.CharField(max_length=32)
    last_name=models.CharField(max_length=30)
    user_name=models.CharField(max_length=30)
    email = models.EmailField()
