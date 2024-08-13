from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Setlist(models.Model):
    title = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    pieces = models.ManyToManyField('library.Piece')

    def save(self, *args, **kwargs):
        self.title = self.title.title()
        super(Setlist, self).save(*args, **kwargs)

    def __str__(self):
        return self.title