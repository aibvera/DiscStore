from django.shortcuts import render
from .models import Album
from django.http import JsonResponse

# Create your views here.

def index(request):
    return render(request, 'index.html')

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
