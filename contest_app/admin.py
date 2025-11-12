from django.contrib import admin
from contest_app.models.problem import Problem

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ['title', 'time_limit']