from imdb.models import *
import json
import copy
import random

def populate_database(actors_list, movies_list, directors_list):
    
    for item in actors_list:
        fb_likes = 0
        if item["fb_likes"]:
            fb_likes = item["fb_likes"]
        Actor.objects.create(
                            actor_id = item["actor_id"],
                            name = item["name"],
                            gender = item["gender"],  
                            fb_likes = fb_likes
                            #age = item["age"],
                            #discription = item["discription"],
                            #image = item["image"]
                            )
    for item in directors_list:
        fb_likes = 0
        if item['no_of_facebook_likes']:
            fb_likes = item['no_of_facebook_likes']
        Director.objects.create(
                            name = item["name"],
                            gender = item["gender"],
                            fb_likes = fb_likes
                            #age = item["age"],
                            #discription = item["discription"],
                            #image = item["image"]
                            )
        
    for item in movies_list:
        budget = 0
        if item['budget']:
            budget = item['budget']
        fb_likes = 0
        if item['likes_on_fb']:
            fb_likes = item['likes_on_fb']
        director_obj = Director.objects.get(name = item["director_name"])
        obj = Movie.objects.create(
                                    movie_id = item["movie_id"], 
                                    name = item["name"],
                                    release_year = item["year_of_release"],
                                    box_office_collection_in_crores = item["box_office_collection_in_crores"], 
                                    genre = random.choice(item["genres"]), 
                                    budget = budget,
                                    fb_likes = fb_likes,
                                    country = item['country'],
                                    language = item['language'],
                                    no_of_users_voted = item['no_of_users_voted'],
                                    average_rating = item['average_rating'],
                                    #result = item["result"],
                                    #discription = item["discription"],
                                    #image = item["image"],
                                    director = director_obj
                                )
        
        list_cast = item["actors"]
        for cast in list_cast:
            actor_obj = Actor.objects.get(actor_id = cast["actor_id"])
            cast_obj = Cast.objects.create(
                                            actor = actor_obj,
                                            movie = obj, role = cast["role"],
                                            is_debut_movie = cast["is_debut_movie"],
                                            #remuneration = cast["remuneration"]
                                            )
            cast_obj.save()

def actor_read_data():
    obj = open("/home/mukunda/Desktop/100_movies/actors_100.json",'r')
    actor_list = obj.read()
    actors_list = json.loads(actor_list)
    return actors_list

def director_read_data():
    obj = open("/home/mukunda/Desktop/complete_data/directors_5000.json",'r')
    director_list = obj.read()
    directors_list = json.loads(director_list)
    return directors_list

def movie_read_data():
    obj = open("/home/mukunda/Desktop/100_movies/movies_100.json",'r')
    movie_list = obj.read()
    movies_list = json.loads(movie_list)
    return movies_list



def get_average_rating_of_movie(movie_obj):
    try:
        rating_obj = Rating.objects.get(movie = movie_obj)
    except Rating.DoesNotExist:
        return 0
    else:
        one_count = movie_obj.rating.rating_one_count
        two_count = movie_obj.rating.rating_two_count
        three_count = movie_obj.rating.rating_three_count
        four_count = movie_obj.rating.rating_four_count
        five_count = movie_obj.rating.rating_five_count
        total_count = one_count + two_count + three_count + four_count + five_count
        if total_count == 0:
            return 0
        else:
            sum = one_count * 1 + two_count * 2 + three_count * 3 + four_count * 4 + five_count * 5
            avg = (sum * 1.0) / total_count
            return round(avg,1)




def execute_sql_query(sql_query):
    """
    Executes sql query and return data in the form of lists (
        This function is similar to what you have learnt earlier. Here we are
        using `cursor` from django instead of sqlite3 library
    )
    :param sql_query: a sql as string
    :return:
    """
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        rows = cursor.fetchall()
    return rows



def get_movie_collections_budget_by_two_bar_plot_data():
    query = """
        SELECT release_year,
                AVG(box_office_collection_in_crores) as collection,
                AVG(budget) as budget
        FROM imdb_movie
        WHERE release_year BETWEEN 2000 AND 2016
        GROUP BY release_year
        """
    list_tuples = execute_sql_query(query)
    movie_collections = []
    movie_budget = []
    movie_year = []
    for item in list_tuples:
        movie_year.append(item[0])
        movie_collections.append(item[1])
        movie_budget.append(item[2])
    multi_bar_plot_data = {
        "labels": list(movie_year),
        "datasets": [
            {
                "label": "Movie Collections",
                "data": list(movie_collections),
                "borderColor": "rgba(0, 123, 255, 0.9)",
                "borderWidth": "0",
                "backgroundColor": "rgb(255, 102, 204, 0.5)",
                "fontFamily": "Poppins"
            },
            {
                "label": "Movie Budget",
                "data": list(movie_budget),
                "borderColor": "rgba(0, 123, 255, 0.9)",
                "borderWidth": "0",
                "backgroundColor": "rgb(153, 255, 51,0.7)",
                "fontFamily": "Poppins"
            }
        ]
    }

    return {
        'multi_bar_plot_data_one': json.dumps(multi_bar_plot_data),
        'multi_bar_plot_data_one_title': 'Collection vs Budget'
    }


def get_multi_line_plot_with_area_data():
    query1 = """
            SELECT release_year,
                    result,
                    count(*)
            FROM imdb_movie 
            GROUP BY release_year,result
            """
    query2 = """SELECT release_year 
                FROM imdb_movie
                GROUP BY release_year
                """
    list1 = execute_sql_query(query1)
    list2 = execute_sql_query(query2)
    year = {}
    result = {'Block Buster':0, 'Average' : 0 , 'Disaster' : 0}
    for item in list2:
        year[item[0]] = copy.deepcopy(result)
    for i in list1:
        if i[1] == 'Block Buster':
            year[i[0]]['Block Buster'] = copy.deepcopy(i[2])
        elif i[1] == 'Average':
            year[i[0]]['Average'] = copy.deepcopy(i[2])
        else:
            year[i[0]]['Disaster'] = copy.deepcopy(i[2])
    label = []
    b_count = []
    a_count = []
    d_count = []
    for v in year.values():
        b_count.append(v['Block Buster'])
        a_count.append(v['Average'])
        d_count.append(v['Disaster'])
    

    multi_line_plot_with_area_data = {
        "labels": list2,
        "defaultFontFamily": "Poppins",
        "datasets": [
            {
                "label": "Block Buster",
                "borderColor": "rgba(0,0,0,.09)",
                "borderWidth": "1",
                "backgroundColor": "rgb(153, 255, 51,0.7)",
                "data": b_count
            },
            {
                "label": "Average",
                "borderColor": "rgba(0, 123, 255, 0.9)",
                "borderWidth": "1",
                "backgroundColor": "rgb(255, 51, 0, 0.5)",
                "pointHighlightStroke": "rgba(26,179,148,1)",
                "data": a_count
            },
            {
                "label": "Disaster",
                "borderColor": "rgba(0, 123, 255, 0.9)",
                "borderWidth": "1",
                "backgroundColor": "rgba(0, 123, 255, 0.5)",
                "pointHighlightStroke": "rgba(26,179,148,1)",
                "data": d_count
            }
        ]
    }

    return {
        'multi_line_plot_with_area_data_one': json.dumps(
            multi_line_plot_with_area_data),
        'multi_line_plot_with_area_data_one_title': 'Movie Results'
    }




def get_movie_collections_by_single_bar_chart():
    query = """
            SELECT release_year,
                count(*)
            FROM imdb_movie
            GROUP BY release_year
            """
    list1 = execute_sql_query(query)
    year = []
    count = []
    for item in list1:
        year.append(item[0])
        count.append(item[1])
    single_bar_chart_data = {
        "labels": year,
        "datasets":[
            {	
                "data": count,
                "label" : "No of movies",
                "borderColor": "rgba(0, 100, 155, 0.9)",
                "border_width": "0",
                "backgroundColor":"rgb(153, 153, 255,0.9)"
            }
        ]
    }
    return {
        'single_bar_chart_data_one': json.dumps(single_bar_chart_data),
        'single_bar_chart_data_one_title': 'No of movies in particular year'
    }




def get_area_plot_data():
    query = """
            SELECT release_year,
                    count(*)
            FROM imdb_movie as m,
            imdb_director as d
            WHERE m.director_id = d.id AND d.id = 3
            GROUP BY release_year
            """
    list1 = execute_sql_query(query)
    year = []
    count = []
    for item in list1:
        year.append(item[0])
        count.append(item[1])
    area_plot_data = {
        "labels": year,
        "type": 'line',
        "defaultFontFamily": 'Poppins',
        "datasets": [{
            "data": count,
            "label": "Movies count",
            "backgroundColor": 'rgba(0,103,255,.15)',
            "borderColor": 'rgba(0,103,255,0.5)',
            "borderWidth": 3.5,
            "pointStyle": 'circle',
            "pointRadius": 5,
            "pointBorderColor": 'transparent',
            "pointBackgroundColor": 'rgba(0,103,255,0.5)',
        }, ]
    }
    return {
        'area_plot_data_one': json.dumps(area_plot_data),
        'area_plot_data_one_title': 'Director - Movies'
    }



def get_pie_chart_data():
    query = """
            SELECT round((COUNT(*)*100.0)/(SELECT COUNT(*)
                                    FROM imdb_actor),2) as percent
            FROM imdb_actor
            GROUP BY gender
            ORDER BY gender
            """
    list1 = execute_sql_query(query)
    pie_chart_data = {
        "datasets": [{
            "data": list1,
            "backgroundColor": [
                "rgba(0, 123, 255,0.9)",
                "rgba(0, 123, 255,0.7)",
                "rgba(0, 123, 255,0.5)",
                "rgba(0,0,0,0.07)"
            ],
            "hoverBackgroundColor": [
                "rgba(0, 123, 255,0.9)",
                "rgba(0, 123, 255,0.7)",
                "rgba(0, 123, 255,0.5)",
                "rgba(0,0,0,0.07)"
            ]

        }],
        "labels": [
            "Female",
            "Male"
        ]
    }

    return {
        'pie_chart_data_one': json.dumps(
            pie_chart_data),
        'pie_chart_data_one_title': 'Pecentage of Actors'
    }





def get_multi_line_plot_data():
    query = """
    select release_year,gender,count(*) from imdb_actor as a,imdb_movie as m,imdb_cast as c where a.actor_id = c.actor_id and m.movie_id = c.movie_id group by m.release_year,a.gender;
    """
    query1 = """
    select release_year from imdb_actor as a,imdb_movie as m,imdb_cast as c where a.actor_id = c.actor_id and m.movie_id = c.movie_id group by m.release_year;
    """
    list1 = execute_sql_query(query)
    list2 = execute_sql_query(query1)
    year = {}
    gender = {'F':0,'M':0}
    for item in list2:
        year[item[0]] = copy.deepcopy(gender)
    for y,gender,count in list1:
        if gender == 'F':
            year[y]['F'] = copy.deepcopy(count)
        else:
            year[y]['M'] = copy.deepcopy(count)
    f_count = []
    m_count = []
    for v in year.values():
        f_count.append(v['F'])
        m_count.append(v['M'])
    multi_line_plot_data = {
        "labels": list2,
        "type": 'line',
        "defaultFontFamily": 'Poppins',
        "datasets": [{
            "label": "Female count",
            "data": f_count,
            "backgroundColor": 'transparent',
            "borderColor": 'rgba(220,53,69,0.75)',
            "borderWidth": 3,
            "pointStyle": 'circle',
            "pointRadius": 5,
            "pointBorderColor": 'transparent',
            "pointBackgroundColor": 'rgba(220,53,69,0.75)',
        }, {
            "label": "Male Count",
            "data": m_count,
            "backgroundColor": 'transparent',
            "borderColor": 'rgba(40,167,69,0.75)',
            "borderWidth": 3,
            "pointStyle": 'circle',
            "pointRadius": 5,
            "pointBorderColor": 'transparent',
            "pointBackgroundColor": 'rgba(40,167,69,0.75)',
        }]
    }
    return {
        'multi_line_plot_data_one': json.dumps(multi_line_plot_data),
        'multi_line_plot_data_one_title': 'Male and Female Actors'
    }


def get_doughnut_chart_data():
    query = """
    SELECT genre,
        (count(*) * 100.0 )/ (SELECT COUNT(*)
                            FROM imdb_movie) as pecent
    FROM imdb_movie
    GROUP BY genre
    """
    list1 = execute_sql_query(query)
    genre = []
    percent = []
    for item in list1:
        genre.append(item[0])
        percent.append(round(item[1],2))
    doughnut_graph_data = {
        "datasets": [{
            "data": percent,
            "backgroundColor": [
                "rgba(100, 123, 255,0.9)",
                "rgba(150, 123, 255,0.7)",
                "rgba(10, 123, 255,0.5)",
                "rgba(0,0,0,0.07)"
            ],
            "hoverBackgroundColor": [
                "rgba(0, 123, 255,0.9)",
                "rgba(0, 123, 255,0.7)",
                "rgba(0, 123, 255,0.5)",
                "rgba(0,0,0,0.07)"
            ]

        }],
        "labels": genre
    }

    return {
        'doughnut_graph_data_one': json.dumps(doughnut_graph_data),
        'doughnut_graph_data_one_title': 'Percentage of Movies'
    }


def get_movie_collections_by_polar_chart():
    query = """
            SELECT release_year,
                count(*)
            FROM imdb_movie
            GROUP BY release_year
            """
    list1 = execute_sql_query(query)
    year = []
    count = []
    for item in list1:
        year.append(item[0])
        count.append(item[1])
    print(year)
    print(count)
    polar_chart_data = {
        "datasets": [{
            "data": count,
            "backgroundColor": [
                "rgb(204, 0, 204,0.9)",
                "rgba(100, 200, 105,0.8)",
                "rgb(240, 100, 0,0.7)",
                "rgb(153, 102, 51,0.9)",
                "rgba(0, 123, 155,0.5)"
            ]

        }],
        "labels": year
    }
    return {
        'polar_chart_data_one': json.dumps(
            polar_chart_data),
        'polar_chart_data_one_title': 'Movie Collections vs Movies'
    }





    






