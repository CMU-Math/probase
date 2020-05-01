from django.db import models
from django.contrib.auth.models import User

class Problem(models.Model):
    title = models.CharField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="problems")
    creation_time = models.DateTimeField(auto_now_add=True) 

    problem_text = models.CharField(max_length=5000) # problem (in latex)
    answer = models.CharField(max_length=100) # answer (in latex)
    solution = models.CharField(max_length=10000) # solution (in latex)

    update_time = models.DateTimeField(null=True) # time of last update
    update_user = models.ForeignKey(User, null=True, on_delete=models.CASCADE) # user who last updated it

class QualityRating(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="qratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="qratings")
    score = models.IntegerField()

class DifficultyRating(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="dratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dratings")
    score = models.IntegerField()







