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
        result = ""
        if float(item['average_rating']) > 8.0:
            result = 'Block Buster'
        elif float(item['average_rating']) > 5.0:
            result = 'Average'
        else:
            result = 'Disaster'
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
                                    result = result,
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
    obj = open("/home/mukunda/Desktop/complete_data/actors_5000.json",'r')
    actor_list = obj.read()
    actors_list = json.loads(actor_list)
    return actors_list

def director_read_data():
    obj = open("/home/mukunda/Desktop/complete_data/directors_5000.json",'r')
    director_list = obj.read()
    directors_list = json.loads(director_list)
    return directors_list

def movie_read_data():
    obj = open("/home/mukunda/Desktop/complete_data/movies_5000.json",'r')
    movie_list = obj.read()
    movies_list = json.loads(movie_list)
    return movies_list



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
                round(AVG(box_office_collection_in_crores),0) as collection,
                round(AVG(budget / 1000000),0) as budget
        FROM imdb_movie
        WHERE release_year BETWEEN 2010 AND 2016
        GROUP BY release_year
        """
    list_tuples = execute_sql_query(query)
    print(list_tuples)
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
        'multi_bar_plot_data_one_title': 'Collection vs Budget in Crores'
    }


def movie_result_get_multi_line_plot_with_area_data():
    query1 = """
            SELECT release_year,
                    result,
                    count(*)
            FROM imdb_movie 
            WHERE release_year BETWEEN 2010 AND 2016
            GROUP BY release_year,result
            """
    query2 = """SELECT release_year 
                FROM imdb_movie
                WHERE release_year BETWEEN 2010 AND 2016
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
                "backgroundColor": "rgb(0, 204, 0)",
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
                "backgroundColor": "rgb(255, 0, 0)",
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




def no_of_movies_get_by_single_bar_chart():
    query = """
            SELECT release_year,
                count(*)
            FROM imdb_movie
            WHERE release_year BETWEEN 2005 AND 2016
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
                "backgroundColor":"rgb(0, 255, 153)"
            }
        ]
    }
    return {
        'single_bar_chart_data_one': json.dumps(single_bar_chart_data),
        'single_bar_chart_data_one_title': 'No of movies in particular year'
    }




def director_movie_get_area_plot_data():
    query = """
            SELECT release_year,
                    count(*)
            FROM imdb_movie as m,
            imdb_director as d
            WHERE m.director_id = d.id AND d.id = 2
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
            "backgroundColor": 'rgb(255, 153, 255))',
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



def actors_percent_get_pie_chart_data():
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
                "rgb(255, 153, 51)",
                "rgb(255, 102, 153)"
            ],
            "hoverBackgroundColor": [   
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





def male_female_get_multi_line_plot_data_gender():
    query = """
    SELECT release_year,
            gender,
            count(*) 
    FROM imdb_actor as a,
        imdb_movie as m,
        imdb_cast as c 
    WHERE a.actor_id = c.actor_id AND m.movie_id = c.movie_id AND release_year between 2005 AND 2016
    GROUP BY m.release_year,a.gender;
    """
    query1 = """
    select release_year
    from imdb_actor as a,
        imdb_movie as m,
        imdb_cast as c 
    where a.actor_id = c.actor_id and m.movie_id = c.movie_id and release_year between 2005 and 2016
    group by m.release_year;
    """
    list1 = execute_sql_query(query)
    list2 = execute_sql_query(query1)
    year = {}
    gender = {'F':0,'M':0}
    for item in list2:
        year[item[0]] = copy.deepcopy(gender)
    for y,gender,count in list1:
        if gender == 'female':
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
        'multi_line_plot_data_one_title': 'Male and Female Actors Count'
    }



def genre_get_doughnut_chart_data():
    query = """
    SELECT genre,
            AVG(box_office_collection_in_crores)
    FROM imdb_movie
    WHERE genre IN ('Crime','Family','Comedy','Drama','Action','Fantasy')
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
                "rgb(255, 102, 204)",
                "rgb(0, 255, 0)",
                "rgba(150, 100, 250,0.7)",
                "rgb(51, 153, 102)",
                "rgb(255, 0, 0)",
                "rgb(153, 51, 51)",
                "rgb(255, 255, 0)",
                "rgb(153, 0, 255)",
                "rgb(51, 51, 0)",
                "rgb(0, 255, 204)",
                "rgb(204, 204, 0)",
                "rgb(153, 51, 51)"
            ],
            "hoverBackgroundColor": []

        }],
        "labels": genre
    }

    return {
        'doughnut_graph_data_one': json.dumps(doughnut_graph_data),
        'doughnut_graph_data_one_title': 'Collections of Movies By Genre'
    }

def rating_movies():
    query = """
        SELECT release_year,
                round(AVG(average_rating),1) as avg
        FROM imdb_movie
        WHERE release_year BETWEEN 2010 AND 2016
        GROUP BY release_year;
        """
    list1 = list1 = execute_sql_query(query)
    year = []
    rating = []
    for item in list1:
        year.append(item[0])
        rating.append(item[1])
    multi_line_plot_data = {
        "labels": year,
        "type": 'line',
        "defaultFontFamily": 'Poppins',
        "datasets": [{
            "label": "Movies_Rating",
            "data": rating,
            "backgroundColor": 'transparent',
            "borderColor": 'rgba(220,53,69,0.75)',
            "borderWidth": 3,
            "pointStyle": 'circle',
            "pointRadius": 5,
            "pointBorderColor": 'transparent',
            "pointBackgroundColor": 'rgba(220,53,69,0.75)',
        }]
    }
    return {
        'multi_line_plot_data_one': json.dumps(multi_line_plot_data),
        'multi_line_plot_data_one_title': 'Average Rating of Movies'
    }

def movie_rating_get_area_plot_data():
    query = """
        SELECT release_year,
                round(AVG(average_rating),1) as avg
        FROM imdb_movie
        WHERE release_year BETWEEN 2010 AND 2016
        GROUP BY release_year;
        """
    list1 = list1 = execute_sql_query(query)
    year = []
    rating = []
    for item in list1:
        year.append(item[0])
        rating.append(item[1])
    area_plot_data = {
        "labels": year,
        "type": 'line',
        "defaultFontFamily": 'Poppins',
        "datasets": [{
            "data": rating,
            "label": "Movies Ratings",
            "backgroundColor": 'rgb(200, 153, 205))',
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
        'area_plot_data_one_title': 'Movie Ratings'
    }


    





