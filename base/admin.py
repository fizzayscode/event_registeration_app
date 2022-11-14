from django.contrib import admin
from .models import Submission, User, Event
# Register your models here.

admin.site.register(User)
admin.site.register(Event)
admin.site.register(Submission)