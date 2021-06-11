from django.contrib import admin
from .models import School, Grade, Subscriber

# Register your models here.
admin.site.register(School)
admin.site.register(Grade)
admin.site.register(Subscriber)