from django.db import models
from django.utils.timezone import now

class Good(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Application(models.Model):
    name = models.CharField(max_length=200, unique=True)
    date = models.DateTimeField(default=now)
    destination = models.CharField(max_length=200)
    progress = models.CharField(max_length=10, default='draft', choices=[
        ('draft', 'Not submitted yet'), ('submitted', 'Submitted'),
        ('processing', 'Being processed'), ('approved', 'Approved'),
        ('declined', 'Declined')
    ])
    goods = models.ManyToManyField(Good)
    def __str__(self):
        return self.name
