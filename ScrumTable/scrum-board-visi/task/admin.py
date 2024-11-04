from django.contrib import admin
from . import models

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'section',
        'create_date',
        'due_date',
    )


class TaskUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'task',
        'user',
    )


admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.TaskUser, TaskUserAdmin)
