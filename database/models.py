from django.db import models
from django.db.models import Avg, Sum
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from taggit.managers import TaggableManager

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
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def avg_diff(self):
        ratings = self.ratings.all()
        return ratings.aggregate(Avg('difficulty'))['difficulty__avg']

    def avg_diff_text(self):
        avg = self.avg_diff()
        if avg is None:
            return 'None'
        avg = round(avg)
        return Rating.DIFF[avg]

    def diff_distribution(self):
        dist = [self.ratings.filter(difficulty=d).count() for d in Rating.DIFF]
        m = max(dist) + 0.00001 # in case there are no ratings
        return dist, [round(i/m*100) for i in dist]

    def avg_qual(self):
        ratings = self.ratings.all()
        s = ratings.aggregate(Sum('quality'))['quality__sum']
        return s/(ratings.count() + 3)

    def avg_qual_text(self):
        avg = self.avg_qual()
        if avg is None:
            return 'None'

        # the 0.5 and 1 cutoffs are a bit arbitrary, they can be changed later if needed
        if abs(avg) < 0.5:
            return Rating.QUAL[0]
        elif abs(avg) < 1:
            if avg > 0:
                return Rating.QUAL[1]
            else:
                return Rating.QUAL[-1]
        else:
            if avg > 0:
                return Rating.QUAL[2]
            else:
                return Rating.QUAL[-2]

    def qual_distribution(self):
        qual = [self.ratings.filter(quality=q).count() for q in Rating.QUAL]
        m = max(qual) + 0.00001 # in case there are no ratings
        return qual, [round(i/m*100) for i in qual]

    def tag_list_text(self):
        return u", ".join(o.name for o in self.tags.all())


class Rating(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ratings")
    VERY_EASY = 1
    EASY = 2
    MED_DIFF = 3
    HARD = 4
    VERY_HARD = 5
    DIFF = {
        VERY_EASY: 'Easy - Mid AMC',
        EASY: 'Easy AIME',
        MED_DIFF: 'Mid AIME',
        HARD: 'Hard AIME',
        VERY_HARD: 'USAMO',
    }
    VERY_GOOD = 2
    GOOD = 1
    MED_QUAL = 0
    BAD = -1
    VERY_BAD = -2
    QUAL = {
        VERY_GOOD: 'Definitely',
        GOOD: 'Yes',
        MED_QUAL: 'Unsure',
        BAD: 'No',
        VERY_BAD: 'Definitely not',
    }
    COLORS = ['#00c853', '#aeea00', '#fdd835', '#ff8f00', '#f4511e']
    difficulty = models.SmallIntegerField(choices=[(k,v) for k,v in DIFF.items()])
    quality = models.SmallIntegerField(choices=[(k,v) for k,v in QUAL.items()])

    def __str__(self):
        return '{} rated {}'.format(self.user, self.problem)

class Comment(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    text = models.CharField(max_length=500) # comment text (in html)
    # max_length of comment text isn't actually enforced

    creation_time = models.DateTimeField(auto_now_add=True) 
    update_time = models.DateTimeField(null=True) # time of last update
    update_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name="+") # user who last updated it
