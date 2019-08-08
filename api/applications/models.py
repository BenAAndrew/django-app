from django.db import models
from django.utils.timezone import now
from goods.models import Good
from users.models import User


class Application(models.Model):
    name = models.CharField(max_length=200, unique=True)
    date = models.DateTimeField(default=now, auto_created=True)
    destination = models.CharField(max_length=200)
    progress = models.CharField(max_length=10, default='draft', choices=[
        ('draft', 'Not submitted yet'), ('submitted', 'Submitted'),
        ('processing', 'Being processed'), ('approved', 'Approved'),
        ('declined', 'Declined')
    ])
    goods = models.ManyToManyField(Good)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
