from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test

def register_view(request):
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('catalogo')
    else:
        user_form = UserCreationForm()
    user_form = UserCreationForm()
    return render(request, 'register.html', {'user_form':user_form})

def register_view(request):
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('login')
    else:
        user_form = CustomUserCreationForm()
    return render(request, 'register.html', {'user_form': user_form})

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('catalogo')
        else:
            login_form = AuthenticationForm()
    else:
        login_form = AuthenticationForm()
    return render(request, 'login.html', {'login_form':login_form})

def custom_logout(request):
    logout(request)
    messages.success(request, "Você saiu com sucesso.")
    return redirect('home')

@login_required
@user_passes_test(lambda user: user.is_superuser)
def painel_view(request):
    return render(request, 'painel.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def catalogo_view(request):
    return render(request, 'catalogo.html')

def home_view(request):
    return render(request, 'home.html')

def detalhes_view(request):
    return render(request, 'detalhes.html')

def editar_view(request):
    return render(request, 'editar.html')