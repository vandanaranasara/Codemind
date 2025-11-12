from django.db import models
from django.conf import settings  # Use custom user model
from contest_app.models.problem import Problem

class LeaderboardEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    time_taken = models.PositiveIntegerField(help_text="Time taken in seconds")
    score = models.IntegerField(default=0)  # 1 = all passed, 0 = failed
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['time_taken', 'submitted_at']  # fastest first
        unique_together = ('user', 'problem')  # one entry per user per problem

    def __str__(self):
        return f"{self.user.username} - {self.problem.title} - {self.score}"