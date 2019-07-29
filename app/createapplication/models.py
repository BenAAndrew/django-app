from django.db import models

class Good(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Application(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField()
    destination = models.CharField(max_length=200)
    goods = models.ManyToManyField(Good)
    def __str__(self):
        return self.name
