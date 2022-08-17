from django.db import models

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=225)
    time = models.DateTimeField(auto_now_add=True)
    temp = models.DecimalField(max_digits=5, decimal_places=2)
    max =  models.DecimalField(max_digits=5, decimal_places=2)
    min =  models.DecimalField(max_digits=5, decimal_places=2)
      # weather_info = models.CharField(max_length=225)

    class Meta:
        verbose_name_plural = "cities"

    def __str__(self):
        return self.name