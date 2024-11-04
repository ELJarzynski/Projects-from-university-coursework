from django.contrib import admin
from . import models
# Register your models here.


class BoardAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "create_date",
        "due_date",
    )


class BoardUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "board",
        "user",
        "is_owner",
    )


admin.site.register(models.Board, BoardAdmin)
admin.site.register(models.BoardUser, BoardUserAdmin)
