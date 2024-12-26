from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=225)
    time = models.DateTimeField(auto_now_add=True)
    temp = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    max = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    min = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "cities"

    def __str__(self):
        return self.name


class ClimateChange(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    time = models.DateField()
    temp = models.FloatField()
    # add more fields as needed
