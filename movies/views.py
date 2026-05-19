from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Movie, Person, Rating, Review
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import RegisterForm, ReviewForm, ProfileForm

def movie_detail(request, movie_id):
    movie = get_object_or_404(
        Movie.objects.prefetch_related('cast', 'crew'),
        id=movie_id
        )
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            return redirect('movie_detail', movie_id=movie.id)
    else:
        form = ReviewForm()
    
    user_rating = 0
    if request.user.is_authenticated:
        existing_rating = Rating.objects.filter(user=request.user, movie=movie).first()
        if existing_rating:
            user_rating = existing_rating.score

    reviews = movie.reviews.all()

    context = {
        'movie': movie,
        'user_rating': user_rating,
        'review_form': form,
        'reviews': reviews,
    }
    return render(request, 'movies/movie_detail.html', context)

def all_movies(request):
    query = request.GET.get('q')
    if query:
        movies_list = Movie.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        ).distinct().order_by('title')
    else:
        movies_list = Movie.objects.all().order_by('title')

    return render(request, 'movies/all_movies.html', {
        'movies': movies_list,
        'query': query
    })

def all_people(request):
    people_list = Person.objects.all().order_by('name')
    
    return render(request, 'movies/all_people.html', {
        'people': people_list
    })

@login_required
def profile_view(request):
    profile = request.user.profile

    if request.method == 'POST':
        # Pass request.FILES to handle profile picture uploads safely
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = ProfileForm(instance=profile)

    context = {
        'profile': profile,
        'profile_form': form,
    }
    return render(request, 'movies/profile.html', context)

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def toggle_watchlist(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    profile = request.user.profile

    if movie in profile.watchlist.all():
        profile.watchlist.remove(movie)
        in_watchlist = False
    else:
        profile.watchlist.add(movie)
        in_watchlist = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'in_watchlist': in_watchlist})

    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def rate_movie(request, movie_id):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, id=movie_id)
        data = json.loads(request.body)
        score = int(data.get('score', 0))

        if 1 <= score <= 5:
            rating, created = Rating.objects.update_or_create(
                user=request.user,
                movie=movie,
                defaults={'score': score}
            )
            return JsonResponse({'success': True, 'score': score})
        
    return JsonResponse({'success': False, 'error': 'Invalid score'}, status=400)