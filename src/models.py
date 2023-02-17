from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class City(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=225)
    time = models.DateTimeField(auto_now_add=True)
    temp = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    max =  models.DecimalField(max_digits=5, decimal_places=2,null=True)
    min =  models.DecimalField(max_digits=5, decimal_places=2,null = True)
      # weather_info = models.CharField(max_length=225)

    class Meta:
        verbose_name_plural = "cities"

    def __str__(self):
        return self.name