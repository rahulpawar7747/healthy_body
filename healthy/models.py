from django.db import models
from django.contrib.auth.models import User

class UserDietPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bmi = models.FloatField()
    status = models.CharField(max_length=50)
    budget = models.IntegerField()
    food_type = models.CharField(max_length=20)
    body_goal = models.CharField(max_length=50, default="General Fitness")
    ai_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
class BMIRecord(models.Model):
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    weight = models.FloatField()
    height = models.FloatField()
    bmi = models.FloatField()
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

class UserHealthPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    diet_reply = models.TextField()
    exercise_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)