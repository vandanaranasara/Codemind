from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from contest_app.models import UserManager, User
from rest_framework_simplejwt.tokens import RefreshToken



def home(request):
    is_logged_in = 'access_token' in request.COOKIES
    return render(request, 'home.html', {'is_logged_in': is_logged_in})



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Signup view
def signup(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        values = {'first_name': firstname, 'last_name': lastname, 'phone': phone, 'email': email}

        if password != confirm_password:
            return render(request, 'signup.html', {'error': "Passwords do not match", 'values': values})

        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': "Email already exists", 'values': values})

        user = User.objects.create_user(email=email, first_name=firstname, last_name=lastname, phone=phone, password=password)

        tokens = get_tokens_for_user(user)
        response = redirect('home')
        response.set_cookie('access_token', tokens['access'])
        response.set_cookie('refresh_token', tokens['refresh'])
        return response

    return render(request, 'signup.html')

# Login view
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        values = {'email': email}

        # user = authenticate(request, email=email, password=password)
        # user = authenticate(request, username=email, password=password)
        user = authenticate(request, email=email, password=password)


        if user is not None:
            tokens = get_tokens_for_user(user)
            response = redirect('home')
            response.set_cookie('access_token', tokens['access'])
            response.set_cookie('refresh_token', tokens['refresh'])
            return response
        else:
            return render(request, 'login.html', {'error': "Invalid Credentials", 'values': values})

    return render(request, 'login.html')


def logout_view(request):
    response = redirect('home')
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response



