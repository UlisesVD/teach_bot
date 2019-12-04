from django.db import models
from users.models import CustomUser
from datetime import datetime


# Create your models here.
class Course(models.Model):
    name = models.CharField(verbose_name='Nombre del Curso', max_length=255)
    description = models.TextField(verbose_name='Descripcion del curso')
    date_start = models.DateTimeField(default = datetime.now, verbose_name='Fecha de Creacion')
    date_end = models.DateTimeField(verbose_name='Fecha de fin de curso')
    id_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Unity(models.Model):
    name = models.CharField(verbose_name='Nombre de la unidad', max_length=255)
    description = models.TextField(verbose_name='Descripcion de la unidad')
    date_start = models.DateTimeField(default = datetime.now, verbose_name='Fecha de inicio')
    date_end = models.DateTimeField(verbose_name='Fecha de fin de unidad')
    id_course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Exam(models.Model):
    title = models.CharField(verbose_name='Titulo del examen', max_length=255)
    date_application = models.DateTimeField(verbose_name='Fecha aplicaion del examen')
    id_unity = models.ForeignKey(Unity, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Question(models.Model):
    question = models.TextField(verbose_name='Pregunta')
    date_start = models.DateTimeField(default = datetime.now, verbose_name='Fecha de inicio')
    type = models.TextField(verbose_name='tipo')
    id_exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

    def __str__(self):
        return self.question

class Answer(models.Model):
    answer = models.TextField(verbose_name='respuesta')
    is_correct = models.BooleanField(verbose_name='Es correcta')
    id_question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer
