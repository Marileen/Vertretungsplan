from django.db import models
from django.core.exceptions import ValidationError


class School(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Subscriber(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)
    # phone = models.CharField(max_length=200, unique=True)
    phone = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    grade = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.school.name
