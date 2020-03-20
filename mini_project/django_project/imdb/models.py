from django.db import models


class Actor(models.Model):
    GENDER = (
        ('F','female'),
        ('M','male'),
    )
    actor_id = models.CharField(max_length = 100, primary_key = True)
    name = models.CharField(max_length = 100)
    gender = models.CharField(max_length = 20, choices = GENDER,null = True)
    age = models.IntegerField(null = True,default = 30)
    fb_likes = models.IntegerField(null = True)
    discription = models.TextField(null = True,blank = True)
    image = models.ImageField(null = True, blank = True)
    def __str__(self):
        return self.actor_id
    
class Director(models.Model):
    GENDER = (
        ('F','female'),
        ('M','male'),
    )
    name = models.CharField(max_length = 100, unique = True)
    gender = models.CharField(max_length = 20, choices = GENDER,null = True)
    age = models.IntegerField(null = True)
    fb_likes = models.IntegerField(null = True)
    discription = models.TextField(null = True,blank = True)
    image = models.ImageField(null = True,blank = True)
    def __str__(self):
        return self.name
    
class Movie(models.Model):
    name = models.CharField(max_length = 100)
    movie_id = models.CharField(max_length = 100, primary_key = True)
    release_year = models.CharField(max_length = 10,null = True)
    fb_likes = models.IntegerField(null = True)
    average_rating = models.FloatField(null = True)
    country = models.CharField(max_length = 50,null = True)
    language = models.CharField(max_length = 50,null = True)
    no_of_users_voted = models.IntegerField(null = True)
    box_office_collection_in_crores = models.FloatField()
    budget = models.FloatField(null = True)
    discription = models.TextField(null = True,blank = True)
    genre = models.CharField(max_length = 50,null = True)
    result = models.CharField(max_length = 30,null = True)
    image = models.ImageField(null = True,blank = True)
    director = models.ForeignKey(Director, on_delete = models.CASCADE)
    actors = models.ManyToManyField(Actor, through = 'imdb.Cast')

class Cast(models.Model):
    actor = models.ForeignKey(Actor, on_delete = models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete = models.CASCADE)
    role = models.CharField(max_length = 50)
    remuneration = models.FloatField(null = True)
    is_debut_movie = models.BooleanField(default = False)
    
