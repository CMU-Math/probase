from django.db import models
from django.db.models import Avg, Sum
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

class Problem(models.Model):
    title = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="problems")
    creation_time = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(
        max_length = 5,
        choices = [
            ('', 'Choose...'),
            ('alg', 'Algebra'),
            ('nt', 'Number Theory'),
            ('geo', 'Geometry'),
            ('combo', 'Combinatorics'),
            ('cs', 'Computer Science'),
            ('other', 'Other'),
        ])

    problem_text = models.CharField(max_length=1000) # problem (in latex)
    answer = models.CharField(max_length=100) # answer (in latex)
    solution = models.CharField(max_length=2000) # solution (in latex)

    update_time = models.DateTimeField(null=True) # time of last update
    update_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name="+") # user who last updated it

    def __str__(self):
        return self.title

    def avg_difficulty(self):
        ratings = self.ratings.all()
        return ratings.aggregate(Avg('difficulty'))['difficulty__avg']

    def avg_quality(self):
        ratings = self.ratings.all()
        return ratings.aggregate(Avg('quality'))['quality__avg']

class Rating(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+")
    difficulty = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    quality = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

class Comment(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+")
    text = models.CharField(max_length=1000) # comment text (in latex)

    creation_time = models.DateTimeField(auto_now_add=True) 
    update_time = models.DateTimeField(null=True) # time of last update
    update_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name="+") # user who last updated it
