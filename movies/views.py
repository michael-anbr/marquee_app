from django.shortcuts import render, get_object_or_404
from .models import Movie

def movie_detail(request, movie_id):
    movie = get_object_or_404(
        Movie.objects.prefetch_related('cast', 'crew'),
        id=movie_id
        )

    context = {
        'movie': movie,
    }

    return render(request, 'movies/movie_detail.html', context)