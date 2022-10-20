from django.urls import path
from .views import *
from udemy import views

app_name = 'udemy'

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('search', SearchView.as_view(), name='search'),
    path('cursos', CursosListView.as_view(), name='cursos'),

]
