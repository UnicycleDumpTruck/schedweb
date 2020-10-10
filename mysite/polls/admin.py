from django.contrib import admin

from .models import Question, Task_Type, Task

admin.site.register(Question)
admin.site.register(Task_Type)
admin.site.register(Task)

# Register your models here.
