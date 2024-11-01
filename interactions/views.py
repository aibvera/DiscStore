from django.shortcuts import render, redirect
from .models import Album
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.conf import settings


# Vistas web #


def catalog(request):
    return render(request, 'index.html')


def index(request):
    if request.user.is_authenticated:
        last_login = request.session.get('last_login')
        if last_login:
            # Convertir la cadena de vuelta a un objeto datetime
            last_login_time = timezone.datetime.fromisoformat(last_login)
            time_since_last_login = (timezone.now() - last_login_time).total_seconds()
            # Cerrar sesión si ha caducado
            if time_since_last_login > 300:  # 5 minutos
                logout(request)
                return render(request, 'index.html')

        # Si la sesión está activa, actualizar la última hora de inicio de sesión y guardarla como cadena
        request.session['last_login'] = timezone.now().isoformat()
        return render(request, 'index.html')


def loginn(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Guardar el tiempo de inicio de sesión como cadena y entrar
            request.session['last_login'] = timezone.now().isoformat()
            return redirect('index')

    return render(request, 'login.html')


def account(request):
    if request.user.is_authenticated:
        return render(request, 'account.html', {'username': request.user.username})
    return redirect('index')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        # Verificar que las contraseñas coincidan
        if password != password_confirm:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'register.html')

        # Verificar si ya existe el nombre de usuario o email
        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
            return render(request, 'register.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, "El email ya está en uso.")
            return render(request, 'register.html')

        # Crear el nuevo usuario
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Redirigir a la página de inicio de sesión
        messages.success(request, "Registro exitoso. Ahora puedes iniciar sesión.")
        return redirect('index')

    return render(request, 'register.html')


# Data #


def get_albums(request):
    albums = Album.objects.select_related('Id_Artist').values(
        'Album_Name', 'Id_Artist__Artist_Name', 'Album_MainGenre', 'Album_Price', 'Album_Cover_Path'
    )
    # Convertir el valor abreviado al nombre completo:
    genre_dict = dict(Album.genre_choices)
    for album in albums:
        album['Album_MainGenre'] = genre_dict[album['Album_MainGenre']]
        album['Album_Cover_Path'] = request.build_absolute_uri(settings.STATIC_URL + album['Album_Cover_Path'])
    data = {
        'message': 'Success',
        'albums': list(albums)
    }
    return JsonResponse(data)
