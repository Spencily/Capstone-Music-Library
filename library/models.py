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

    def save(self, *args, **kwargs):
        self.title = self.title.capitalize()
        self.composer = self.composer.capitalize()
        self.arranged_by = self.arranged_by.capitalize()
        self.genre = self.genre.capitalize()
        self.mc_location = self.mc_location.capitalize()

        super(Piece, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
