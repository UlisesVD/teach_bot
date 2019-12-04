from django.urls import path
from .views import CreateCourse
from . import views

courses_patterns = ([
    path("create/", CreateCourse.as_view(), name= "createcourse"),
    path("delete_course/", views.delete_course, name='delete_course'),
    path("update/<int:id_course>/", views.update_course, name="update_course"),
    path("<int:id>/<slug:title>/", views.detail, name='unities'),
    path("<int:id_unity>/<int:id_course>/<slug:title>/", views.delete_unity, name='delete_unity'),
    path("update_unity/<int:id_unity>/<int:id_course>/<slug:title>/", views.update_unity, name='update_unity'),
    path("create_exam/", views.create_exam, name='create_exam'),
    path("save_exam/", views.save_exam, name="save_examn"),
], 'courses')
