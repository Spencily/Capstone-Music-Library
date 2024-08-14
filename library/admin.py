from django.contrib import admin
from .models import Part, Piece


# Register your models here.
@admin.register(Piece)
class PieceAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "composer",
        "arranged_by",
        "genre",
        "mc_location",
        "band_arrangement",
    )
    list_filter = (
        "title",
        "composer",
        "arranged_by",
        "genre",
        "mc_location",
        "band_arrangement",
    )
    search_fields = (
        "title",
        "composer",
        "arranged_by",
        "genre",
        "mc_location",
        "band_arrangement",
    )
    ordering = (
        "title",
        "composer",
        "arranged_by",
        "genre",
        "mc_location",
        "band_arrangement",
    )
    list_per_page = 25


@admin.register(Part)
class PartsAdmin(admin.ModelAdmin):
    list_display = ("instrument", "part_number", "piece")
    list_filter = ("instrument", "part_number", "piece")
    search_fields = ("instrument", "part_number", "piece")
    ordering = ("instrument", "part_number", "piece")
    list_per_page = 25
