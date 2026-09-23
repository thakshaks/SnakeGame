# main/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Score

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto log-in after signup
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard_view(request):
    # Retrieve top 5 scores for Snake and Tetris across all users
    top_snake = Score.objects.filter(game_name='snake').select_related('user').order_by('-score')[:5]
    top_tetris = Score.objects.filter(game_name='tetris').select_related('user').order_by('-score')[:5]

    # Retrieve current user's best score for each game
    user_snake_best = Score.objects.filter(user=request.user, game_name='snake').order_by('-score').first()
    user_tetris_best = Score.objects.filter(user=request.user, game_name='tetris').order_by('-score').first()

    context = {
        'top_snake': top_snake,
        'top_tetris': top_tetris,
        'user_snake_best': user_snake_best.score if user_snake_best else 0,
        'user_tetris_best': user_tetris_best.score if user_tetris_best else 0,
    }
    return render(request, 'main/dashboard.html', context)

@login_required(login_url='login')
def game_view(request, game_name):
    return render(request, f'main/{game_name}.html')