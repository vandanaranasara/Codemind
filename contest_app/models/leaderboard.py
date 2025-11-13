from django.db import models
from django.conf import settings 
from contest_app.models.problem import Problem

class LeaderboardEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    time_taken = models.PositiveIntegerField(help_text="Time taken in seconds")
    score = models.IntegerField(default=0) 
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['time_taken', 'submitted_at']  
        unique_together = ('user', 'problem')  # one entry per user per problem

    def __str__(self):
        return f"{self.user.username} - {self.problem.title} - {self.score}"