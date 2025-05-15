from django.db import models

from django.db import models


# Create your models here.

class JsonData(models.Model):
    name = models.CharField(max_length=49, verbose_name="Имя")
    date = models.DateTimeField(verbose_name="Дата")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Запись JSON"
        verbose_name_plural = "Записи JSON"
