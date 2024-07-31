from django.db import models

# Create your models here.
class Setlist(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    pieces = models.ManyToManyField('library.Piece')

    def __str__(self):
        return self.title