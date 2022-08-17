from django.db import models

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=225,null=True, default="freedom land")
    time = models.DateTimeField(auto_now_add=True)
    temperature = models.IntegerField(null=True)
    # weather_info = models.CharField(max_length=225)

    class Meta:
        verbose_name_plural = "cities"

    def __str__(self):
        return self.name