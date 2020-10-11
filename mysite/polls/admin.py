from django.contrib import admin

from .models import Question, Task_Type, Task, Exhibit

admin.site.register(Question)
admin.site.register(Task_Type)
admin.site.register(Task)
admin.site.register(Exhibit)

# Register your models here.
