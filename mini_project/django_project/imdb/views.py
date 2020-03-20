from django.shortcuts import render
from .models import *
from .utils import *
def home(request):
    movie_list = Movie.objects.all()
    return render(request,'imdb_home.html',{'movie_list': movie_list})

def movie(request,movie_id):
    mov_obj = Movie.objects.get(movie_id = movie_id)
    actors_list = mov_obj.actors.all()
    context = {'movie' : mov_obj,'actors_list' : actors_list}
    return render(request,'imdb_movie.html',context)

def actor(request,actor_id):
    act_obj = Actor.objects.get(actor_id = actor_id)
    movies_list = act_obj.movie_set.all()
    context = {'actor' : act_obj , 'movies_list' : movies_list}
    return render(request,'imdb_actor.html',context)

def director(request,director_id):
    dir_obj = Director.objects.get(id = director_id)
    movies_list = dir_obj.movie_set.all()
    context = {'director' : dir_obj, 'movies_list': movies_list}
    return render(request,'imdb_director.html',context)


def analytics(request):
    graphs = {}
    collection_budget = get_movie_collections_budget_by_two_bar_plot_data()
    movie_result = movie_result_get_multi_line_plot_with_area_data()
    no_of_movies = no_of_movies_get_by_single_bar_chart()
    director_movie = director_movie_get_area_plot_data()
    actors_percent = actors_percent_get_pie_chart_data()
    male_femal_count = male_female_get_multi_line_plot_data_gender()
    genre = genre_get_doughnut_chart_data()
    rating_movie = movie_rating_get_area_plot_data()
    graphs.update(collection_budget)
    graphs.update(movie_result)
    graphs.update(no_of_movies)
    graphs.update(director_movie)
    graphs.update(actors_percent)
    graphs.update(male_femal_count)
    graphs.update(genre)
    graphs.update(rating_movie)
    return render(request,'analytics.html',context = graphs)


def all_movie(request):
    list_movies = Movie.objects.all()
    return render(request,'imdb_all_movie.html',{'movie_list' : list_movies})

def all_actor(request):
    list_actors = Actor.objects.all()
    return render(request,'imdb_all_actor.html',{'list_actors' : list_actors})

def all_director(request):
    list_directors = Director.objects.all()
    return render(request,'imdb_all_director.html',{'list_directors' : list_directors})




