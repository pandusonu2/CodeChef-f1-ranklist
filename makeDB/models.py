from django.db import models

# Create your models here.

class Score(models.Model):
    contest = models.CharField(max_length=10)
    points = models.PositiveSmallIntegerField(default=0, null=False)
    def __str__(self):
        return self.contest + ":" + str(self.points)
    class Meta:
        ordering = ('contest',)

class User(models.Model):
    userName = models.CharField(max_length=100, primary_key=True)
    score = models.ManyToManyField(Score)
    def __str__(self):
        return self.userName
    class Meta:
        ordering = ('userName',)