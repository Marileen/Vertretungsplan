from django.db import models


# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Grade(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=4)

    def __str__(self):
        return self.name


class Subscriber(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)
    telefon = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)