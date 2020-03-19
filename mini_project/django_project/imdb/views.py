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
    single_bar_chart = get_movie_collections_by_single_bar_chart()
    two_bar_chart = get_movie_collections_budget_by_two_bar_plot_data()
    multi_bar_chart = get_multi_line_plot_data()
    area_plot = get_area_plot_data()
    multi_area = get_multi_line_plot_with_area_data()
    pie_chart = get_pie_chart_data()
    doughnut = get_doughnut_chart_data()
    single_bar_chart.update(single_bar_chart)
    single_bar_chart.update(two_bar_chart)
    single_bar_chart.update(multi_bar_chart)
    single_bar_chart.update(area_plot)
    single_bar_chart.update(multi_area)
    single_bar_chart.update(pie_chart)
    single_bar_chart.update(doughnut)
    return render(request,'analytics.html',context = single_bar_chart)


def all_movie(request):
    list_movies = Movie.objects.all()
    return render(request,'imdb_all_movie.html',{'movie_list' : list_movies})

def all_actor(request):
    list_actors = Actor.objects.all()
    return render(request,'imdb_all_actor.html',{'list_actors' : list_actors})

def all_director(request):
    list_directors = Director.objects.all()
    return render(request,'imdb_all_director.html',{'list_directors' : list_directors})



