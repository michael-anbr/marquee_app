from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify


class Person(models.Model):
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to="people/", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    has_profile = models.BooleanField(default=False)
    slug = models.SlugField(max_length=250, unique=True, blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def first_letter(self):
        return self.name[0].upper() if self.name else "#"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class MovieCast(models.Model):
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    character_name = models.CharField(max_length=150)  # Character name lives here now!

    def __str__(self):
        return f"{self.person.name} as {self.character_name}"


class MovieCrew(models.Model):
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)  # e.g., "Director", "Composer"

    def __str__(self):
        return f"{self.person.name} - {self.role}"


class Movie(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    year = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    poster = models.ImageField(upload_to="posters/", blank=True, null=True)
    cast = models.ManyToManyField(
        Person, through="MovieCast", related_name="acting_credits", blank=True
    )
    crew = models.ManyToManyField(
        Person, through="MovieCrew", related_name="crew_credits", blank=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.year})"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE, related_name="reviews")
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Review by {self.user.username} on {self.movie.title}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pics/", blank=True, null=True
    )
    watchlist = models.ManyToManyField("Movie", blank=True, related_name="watched_by")

    def __str__(self):
        return f"{self.user.username}'s Profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, "profile"):
        instance.profile.save()
    else:
        Profile.objects.create(user=instance)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE, related_name="ratings")
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "movie")

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}: {self.score} Stars"
