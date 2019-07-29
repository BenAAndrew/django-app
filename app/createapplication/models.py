from django.db import models

class Application(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField()
    destinaton = models.CharField(max_length=200)
    def __str__(self):
        return self.name
