from django.db import models
from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator, MaxValueValidator


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
        self.title = self.title.title()
        self.composer = self.composer.title()
        self.arranged_by = self.arranged_by.capitalize()
        self.genre = self.genre.capitalize()
        self.mc_location = self.mc_location.capitalize()

        super(Piece, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class Part(models.Model):
    instrument = models.CharField(max_length=100)
    part_number = models.SmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='parts')
    pdf_file = CloudinaryField('pdf_file')

    def save(self, *args, **kwargs):
        self.instrument = self.instrument.title()

        super(Part, self).save(*args, **kwargs)
