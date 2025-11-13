from django.shortcuts import render, get_object_or_404
from contest_app.models.problem import Problem
from django.http import JsonResponse
from contest_app.models.leaderboard import LeaderboardEntry
from django.contrib.auth import get_user_model
from django.utils import timezone
import json

def problem_list(request):
    problems = Problem.objects.all()
    return render(request, 'problem_list.html', {'problems': problems})

def problem_detail(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    return render(request, 'problem_detail.html', {'problem': problem})

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken

def get_user_from_token(request):
    token = request.COOKIES.get('access_token')
    if not token:
        return None
    try:
        access = AccessToken(token)
        User = get_user_model()
        user = User.objects.get(id=access['user_id'])
        return user
    except:
        return None

def submit_code(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method."}, status=405)

    user = get_user_from_token(request)
    if not user:
        return JsonResponse({"error": "User must be logged in to submit code."}, status=401)

    data = json.loads(request.body)
    code = data.get("code", "").strip()
    problem_id = data.get("problem_id")
    time_taken = int(data.get("time_taken", 0))

    problem = get_object_or_404(Problem, id=problem_id)

    # Run code tests
    all_passed = True  # Replace with actual test logic
    score = 1 if all_passed else 0

    if score == 1:
        LeaderboardEntry.objects.update_or_create(
            user=user,
            problem=problem,
            defaults={
                "time_taken": time_taken,
                "score": score,
                "submitted_at": timezone.now()
            }
        )

    return JsonResponse({"success": True, "score": score})