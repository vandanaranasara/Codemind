from django.db import models

class Problem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    sample_input = models.TextField()
    sample_output = models.TextField()
    hidden_test_cases = models.TextField()
    time_limit = models.CharField(max_length=50)

    def __str__(self):
        return self.title