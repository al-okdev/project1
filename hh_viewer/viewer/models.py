from django.db import models

# Create your models here.
class Vacancy(models.Model):
    experiece = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    competentions = models.TextField(blank=True, null=True)