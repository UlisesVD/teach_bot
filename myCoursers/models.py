from django.db import models
from users.models import CustomUser
from courses.models import Course

# Create your models here.
class MyCourses(models.Model):
    id_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    id_course = models.ForeignKey(Course, on_delete=models.CASCADE)

