from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from movies.models import Movie


def home(request):
    carousel_movies = Movie.objects.all()[:5]

    what_to_watch = Movie.objects.all()

    context = {
        "carousel_movies": carousel_movies,
        "what_to_watch": what_to_watch,
    }
    return render(request, "marquee_app/index.html", context)


def movie_list(request):
    query = request.GET.get("search", "").strip()
    movies = Movie.objects.all()

    if query:
        movies = movies.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        ).distinct()

    return render(request, "movies/movie_list.html", {"movies": movies, "query": query})


def movie_detail(request, pk):
    movie = get_object_or_404(Movie.objects.prefetch_related("cast", "crew"), pk=pk)

    return render(request, "movies/movie_detail.html", {"movie": movie})
