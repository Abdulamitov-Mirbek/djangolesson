from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Student(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    age = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(120)]
    )

    def __str__(self):
        return self.name
