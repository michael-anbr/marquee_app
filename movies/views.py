from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Value
from django.db.models.functions import Replace, Lower
from .models import Movie, Person, Rating, Review
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.http import HttpResponseForbidden
from .forms import RegisterForm, ReviewForm, ProfileForm, ChangeUsernameForm


def movie_detail(request, slug):
    movie = get_object_or_404(Movie.objects.prefetch_related("cast", "crew"), slug=slug)

    if request.method == "POST" and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            return redirect("movies:movie_detail", slug=movie.slug)
    else:
        form = ReviewForm()

    user_rating = 0
    if request.user.is_authenticated:
        existing_rating = Rating.objects.filter(user=request.user, movie=movie).first()
        if existing_rating:
            user_rating = existing_rating.score

    reviews = movie.reviews.all()

    context = {
        "movie": movie,
        "user_rating": user_rating,
        "review_form": form,
        "reviews": reviews,
    }
    return render(request, "movies/movie_detail.html", context)


def all_movies(request):
    query = request.GET.get("q", "").strip()  # Clean leading/trailing spaces

    if query:
        clean_query = query.lower().replace(" ", "").replace("-", "").replace(":", "")

        annotated_movies = (
            Movie.objects.annotate(
                no_spaces_title=Replace(Lower("title"), Value(" "), Value(""))
            )
            .annotate(
                no_hyphens_title=Replace("no_spaces_title", Value("-"), Value(""))
            )
            .annotate(clean_title=Replace("no_hyphens_title", Value(":"), Value("")))
        )

        movies_list = (
            annotated_movies.filter(
                Q(clean_title__icontains=clean_query) | Q(description__icontains=query)
            )
            .distinct()
            .order_by("title")
        )

    else:
        movies_list = Movie.objects.all().order_by("title")

    return render(
        request, "movies/all_movies.html", {"movies": movies_list, "query": query}
    )


def all_people(request):
    people_list = Person.objects.all().order_by("name")

    return render(request, "movies/all_people.html", {"people": people_list})


@login_required
def profile_view(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("movies:user_profile")
    else:
        form = ProfileForm(instance=profile)

    context = {
        "profile": profile,
        "profile_form": form,
        "watchlist": profile.watchlist.all(),
    }
    return render(request, "movies/profile.html", context)


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def toggle_watchlist(request, movie_slug):
    movie = get_object_or_404(Movie, slug=movie_slug)
    profile = request.user.profile

    if movie in profile.watchlist.all():
        profile.watchlist.remove(movie)
        in_watchlist = False
    else:
        profile.watchlist.add(movie)
        in_watchlist = True

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"in_watchlist": in_watchlist})

    return redirect(request.META.get("HTTP_REFERER", "home"))


@login_required
def rate_movie(request, movie_id):
    if request.method == "POST":
        movie = get_object_or_404(Movie, id=movie_id)
        data = json.loads(request.body)
        score = int(data.get("score", 0))

        if 1 <= score <= 5:
            rating, created = Rating.objects.update_or_create(
                user=request.user, movie=movie, defaults={"score": score}
            )
            return JsonResponse({"success": True, "score": score})

    return JsonResponse({"success": False, "error": "Invalid score"}, status=400)


def actor_profile(request, slug):
    actor = get_object_or_404(Person, slug=slug)
    return render(request, "movies/actor_profile.html", {"actor": actor})


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if review.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this review.")

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("movies:movie_detail", slug=review.movie.slug)
    else:
        form = ReviewForm(instance=review)

    return render(request, "movies/edit_review.html", {"form": form, "review": review})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if review.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this review.")

    if request.method == "POST":
        movie_slug = review.movie.slug
        review.delete()
        return redirect("movies:movie_detail", slug=movie_slug)

    return render(request, "movies/confirm_delete_review.html", {"review": review})


@login_required
def change_username(request):
    if request.method == "POST":
        form = ChangeUsernameForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your username has been updated successfully!")
            return redirect("movies:user_profile")
    else:
        form = ChangeUsernameForm(instance=request.user)

    return render(request, "movies/change_username.html", {"form": form})


@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your account has been permanently deleted.")
        return redirect("/")

    return render(request, "movies/confirm_delete_account.html")
