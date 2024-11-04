from django.contrib import admin
from . import models

# Register your models here.
class SectionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "board"
    )

admin.site.register(models.Section, SectionAdmin)