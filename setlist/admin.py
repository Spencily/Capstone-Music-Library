from django.contrib import admin
from . models import Setlist

# Register your models here.
@admin.register(Setlist)
class SetlistAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    list_filter = ('title', 'description')
    search_fields = ('title', 'description')
    ordering = ('title', 'description')
    list_per_page = 25