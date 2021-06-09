# define our paths to different web pages
# urls for the different views in views.py file

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index")
]