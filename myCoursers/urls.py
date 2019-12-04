from django.urls import path
from . import views
from .views import MyCoursesListView

my_courses_patterns = ([
    path("addToFavorites/<int:id_course>/", views.addToFaborites, name= "addToFavorites"),
    path("myCoursesList/", MyCoursesListView.as_view(), name="MyCoursesList"),
    path("<int:id>/<slug:title>/", views.detail, name='unities'),
    path("exam/", views.solve_exam, name='exam'),
    path("results/", views.results_exam, name='results'),
], 'myCourses')
