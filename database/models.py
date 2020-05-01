from django.db import models
from django.contrib.auth.models import User

class Problem(models.Model):
    title = models.CharField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="problems")
    creation_time = models.DateTimeField(auto_now_add=True) 

    problem_text = models.CharField(max_length=1000) # problem (in latex)
    answer = models.CharField(max_length=100) # answer (in latex)
    solution = models.CharField(max_length=10000) # solution (in latex)

    update_time = models.DateTimeField(null=True) # time of last update
    update_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="+") # user who last updated it

class QualityRating(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="qratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    score = models.IntegerField()

class DifficultyRating(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="dratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    score = models.IntegerField()

class Comment(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    text = models.CharField(max_length=1000) # comment text (in latex)

    creation_time = models.DateTimeField(auto_now_add=True) 
    update_time = models.DateTimeField(null=True) # time of last update
    update_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="+") # user who last updated it
