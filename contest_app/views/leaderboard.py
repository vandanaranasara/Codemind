from django.shortcuts import render, get_object_or_404
from contest_app.models.leaderboard import LeaderboardEntry
from contest_app.models.problem import Problem

def problem_leaderboard(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    entries = LeaderboardEntry.objects.filter(problem=problem, score=1).order_by('time_taken', 'submitted_at')

    leaderboard_data = []
    for entry in entries:
        hours = entry.time_taken // 3600
        minutes = (entry.time_taken % 3600) // 60
        seconds = entry.time_taken % 60
        leaderboard_data.append({
            "user": entry.user,
            "time_taken": entry.time_taken,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds
        })

    return render(request, "leaderboard.html", {
        "problem": problem,
        "entries": leaderboard_data
    })
