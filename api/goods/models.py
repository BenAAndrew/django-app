from django.core.validators import RegexValidator
from django.db import models
from users.models import User


class Good(models.Model):
    name = models.CharField(max_length=200, validators=[RegexValidator("^[^(0-9)]*$", message="Please don't enter numbers", code="includesNumbers")])
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
