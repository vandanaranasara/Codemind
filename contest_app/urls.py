from django.urls import path
from .views.user import home,signup, login_view, logout_view
from .views.about import about, contact
from .views.problem import problem_list, problem_detail, submit_code
from .views.runcode import run_code
from .views.leaderboard import problem_leaderboard
from .views.admin_leaderboard import admin_leaderboard


urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('problems/', problem_list, name='problem_list'),
    path('problems/<int:pk>/', problem_detail, name='problem_detail'),
    path('problems/submit/', submit_code, name='submit_code'),
    path('run/', run_code, name='run_code'),
    path('leaderboard/<int:problem_id>/', problem_leaderboard, name='leaderboard_detail'),
    path('adminleaderboard/', admin_leaderboard, name='admin_leaderboard' )
]
