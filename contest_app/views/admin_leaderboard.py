from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.db.models import Count
from contest_app.models.leaderboard import LeaderboardEntry


# Only allow staff or superusers
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def admin_leaderboard(request):
    # Count how many problems each user solved (distinct)
    leaderboard_data = (
        LeaderboardEntry.objects
        .values('user__id', 'user__first_name', 'user__last_name', 'user__email')
        .annotate(problems_solved=Count('problem', distinct=True))
        .order_by('-problems_solved', 'user__first_name')
    )

    # Apply tie-aware ranking
    rank = 1
    prev_solved = None
    same_rank_count = 0

    for entry in leaderboard_data:
        if prev_solved is None:
            entry['rank'] = rank
        elif entry['problems_solved'] == prev_solved:
            entry['rank'] = rank  # same rank for tie
            same_rank_count += 1
        else:
            rank += same_rank_count + 1
            entry['rank'] = rank
            same_rank_count = 0
        prev_solved = entry['problems_solved']

    context = {'entries': leaderboard_data}
    return render(request, 'admin_leaderboard.html', context)
 