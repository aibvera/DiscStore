from django.shortcuts import render, redirect
from .models import Album
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.utils import timezone
from .models import Order
from django.http import JsonResponse

# Create your views here.

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
                messages.info(request, "Su sesión ha caducado. Inicie sesión nuevamente.")
                return render(request, 'index.html')
        
        # Si la sesión está activa, actualizar la última hora de inicio de sesión y guardarla como cadena
        request.session['last_login'] = timezone.now().isoformat()
        return redirect('main')
    
    # Si no está autenticado, y ha hecho clic en login:
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Guardar el tiempo de inicio de sesión como cadena y entrar
            request.session['last_login'] = timezone.now().isoformat()
            return redirect('main')
        else:
            messages.error(request, "Credenciales incorrectas.")

    return render(request, 'index.html')  # Mostrar el formulario de inicio de sesión


def main(request):
    # Verificar si el usuario está autenticado
    if not request.user.is_authenticated:
        return redirect('index')
    return render(request, 'main.html', {'username': request.user.username})


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


def catalog(request):
    return render(request, 'catalog.html')


def get_albums(request):
    albums = Album.objects.select_related('Id_Artist').values(
        'Album_Name', 'Id_Artist__Artist_Name', 'Album_MainGenre', 'Album_Price'
    )
    # Convertir el valor abreviado al nombre completo:
    genre_dict = dict(Album.genre_choices)
    for album in albums:
        album['Album_MainGenre'] = genre_dict[album['Album_MainGenre']]
    data = {
        'message': 'Success',
        'albums': list(albums)
    }
    return JsonResponse(data)
