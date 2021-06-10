from django.db import models


# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Grade(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=4)
