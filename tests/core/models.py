from __future__ import unicode_literals
from __future__ import absolute_import
from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=30, verbose_name="Student's name")
    age = models.IntegerField(verbose_name="Student's age")
    is_graduated = models.BooleanField(default=False, verbose_name="Graduated")
    birthday = models.DateTimeField(verbose_name="Birthday")
    college = models.ForeignKey('College', verbose_name="Students's college", related_name='students')

    def __str__(self):
        return self.name


class College(models.Model):
    name = models.CharField(max_length=30, verbose_name="College's name")
