from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "movies"

urlpatterns = [
    path("movie/<slug:slug>/", views.movie_detail, name="movie_detail"),
    path("all/", views.all_movies, name="all_movies"),
    path("people/", views.all_people, name="all_people"),
    path("people/<slug:slug>/", views.actor_profile, name="actor_profile"),
    path("profile/", views.profile_view, name="user_profile"),
    path("register/", views.register_view, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="movies:all_movies"),
        name="logout",
    ),
    path(
        "movie/<slug:movie_slug>/watchlist/",
        views.toggle_watchlist,
        name="toggle_watchlist",
    ),
    path("movie/<int:movie_id>/rate/", views.rate_movie, name="rate_movie"),
    path("review/<int:review_id>/edit/", views.edit_review, name="edit_review"),
    path("review/<int:review_id>/delete/", views.delete_review, name="delete_review"),
    path("profile/change-username/", views.change_username, name="change_username"),
    path("profile/delete-account/", views.delete_account, name="delete_account"),
    path(
        "profile/password/",
        auth_views.PasswordChangeView.as_view(
            template_name="movies/change_password.html",
            success_url="/movies/profile/password/done/",
        ),
        name="change_password",
    ),
    path(
        "profile/password/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="movies/change_password_done.html"
        ),
        name="password_change_done",
    ),
]
