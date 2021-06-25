from django.contrib import admin
from .models import School, Subscriber, Subscription

# Register your models here.
admin.site.register(School)
admin.site.register(Subscriber)
admin.site.register(Subscription)
