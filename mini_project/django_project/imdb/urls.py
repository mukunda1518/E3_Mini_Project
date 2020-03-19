from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movie/<str:movie_id>/', views.movie, name='movie'),
    path('actor/<str:actor_id>/', views.actor, name='actor'),
    path('director/<str:director_id>/', views.director, name='director'),
    path('analytics/', views.analytics, name='analytics'),
    path('movie/',views.all_movie, name = 'all_movie'),
    path('actor/',views.all_actor, name = 'all_actor'),
    path('director/',views.all_director, name = 'all_director'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
