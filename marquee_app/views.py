from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from movies.models import Movie

def home(request):
    movies = Movie.objects.all()
    return render(request, 'marquee_app/index.html', {'movies': movies})

def movie_list(request):
    query = request.GET.get('search', '').strip()
    movies = Movie.objects.all()

    if query:
        movies = movies.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        ).distinct()

    return render(request, 'movies/movie_list.html', {'movies': movies, 'query': query})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, 'movies/movie_detail.html', {'movie': movie})