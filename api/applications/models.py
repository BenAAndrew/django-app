from django.core.validators import RegexValidator
from django.db import models
from django.utils.timezone import now
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validateNumbers(value):
    if any(s.isdigit() for s in value):
        raise ValidationError(
            _('%(value)s contains a number'),
            params={'value': value},
        )

class Good(models.Model):
    name = models.CharField(max_length=200, validators=[RegexValidator("/^([^0-9]*)$/", message="Please don't enter numbers", code="includesNumbers")])
    def __str__(self):
        return self.name

class Application(models.Model):
    name = models.CharField(max_length=200, unique=True)
    date = models.DateTimeField(default=now)
    destination = models.CharField(max_length=200)
    goods = models.ManyToManyField(Good)
    def __str__(self):
        return self.name
