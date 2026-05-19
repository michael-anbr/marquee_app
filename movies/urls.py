from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('all/', views.all_movies, name='all_movies'),
    path('people/', views.all_people, name='all_people'),
    path('profile/', views.profile_view, name='user_profile'),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('movie/<int:movie_id>/watchlist/', views.toggle_watchlist, name='toggle_watchlist'),
    path('movie/<int:movie_id>/rate/', views.rate_movie, name='rate_movie'),
]