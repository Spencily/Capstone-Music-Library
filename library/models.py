from django.db import models


class Piece(models.Model):
    class BandArrangement(models.TextChoices):
        FULL_BAND = "Full-band", "Full-band"
        FLEXI_BAND = "Flexi-band", "Flexi-band"

    title = models.CharField(max_length=100)
    composer = models.CharField(max_length=100, blank=True)
    arranged_by = models.CharField(max_length=100, blank=True)
    genre = models.CharField(max_length=100)
    mc_location = models.CharField(max_length=100, blank=True)
    band_arrangement = models.CharField(max_length=20, choices=BandArrangement.choices)

    def __str__(self):
        return self.title
