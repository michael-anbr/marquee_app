from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=100, blank=True)
    character_name = models.CharField(max_length=150, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
class MovieCast(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    character_name = models.CharField(max_length=150)  # Character name lives here now!

    def __str__(self):
        return f"{self.person.name} as {self.character_name}"
    
class MovieCrew(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.CharField(max_length=100) # e.g., "Director", "Composer"

    def __str__(self):
        return f"{self.person.name} - {self.role}"

class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    cast = models.ManyToManyField(Person, through='MovieCast', related_name='acting_credits', blank=True)
    crew = models.ManyToManyField(Person, through='MovieCrew', related_name='crew_credits', blank=True)

    def __str__(self):
        return f"{self.title} ({self.year})"  

class Review(models.Model):
    movie = models.ForeignKey(Movie, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movie.title} review"