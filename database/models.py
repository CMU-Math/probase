from django.db import models
from django.contrib.auth.models import User

class Problem(models.Model):
    title = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="problems")
    creation_time = models.DateTimeField(auto_now_add=True) 

    problem_text = models.CharField(max_length=1000) # problem (in latex)
    answer = models.CharField(max_length=100) # answer (in latex)
    solution = models.CharField(max_length=10000) # solution (in latex)

    update_time = models.DateTimeField(null=True) # time of last update
    update_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="+") # user who last updated it

    def __str__(self):
        return self.title

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

def full_name(self):
    return self.first_name + " " + self.last_name

User.add_to_class("__str__", full_name)
