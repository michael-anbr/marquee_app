from django import template
from movies.models import Rating

register = template.Library()

@register.filter
def get_user_rating(movie, user):
    if user.is_authenticated:
        rating = Rating.objects.filter(movie=movie, user=user).first()
        if rating:
            return range(rating.score)
    return range(0)