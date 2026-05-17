from django.contrib import admin
from .models import Movie, Person, MovieCrew, MovieCast

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ['name']

class MovieCastInline(admin.TabularInline):
    model = MovieCast
    extra = 1
    autocomplete_fields = ['person']

class MovieCrewInline(admin.TabularInline):
    model = MovieCrew
    extra = 1
    autocomplete_fields = ['person']

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    inlines = [MovieCastInline, MovieCrewInline]