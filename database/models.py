from django.db import models
from django.contrib.auth.models import User

class Problem(models.Model):
    title = models.CharField(max_length=200, unique=True)
    author = models.ForeignKey(User, related_name="problems", on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True) 

    problem_text = models.CharField(max_length=5000) # problem (in latex)
    answer = models.CharField(max_length=100) # answer (in latex)
    solution = models.CharField(max_length=10000) # solution (in latex)

    difficulty = models.FloatField() # average difficulty rating
    difficulty_votes = models.IntegerField() # number of people who rated it
    quality = models.FloatField() # average quality rating
    quality_votes = models.IntegerField() # number of people who rated it

    update_time = models.DateTimeField(null=True) # time of last update
    update_user = models.ForeignKey(User, null=True, on_delete=models.CASCADE) # user who last updated it




