from __future__ import unicode_literals
from __future__ import absolute_import
import datetime

from django.db import models

from tests.core.models import College, Student


def create_student_and_get_queryset():
    college1, _ = College.objects.get_or_create(name="College 1st")
    college2, _ = College.objects.get_or_create(name="College 2nd")

    Student.objects.get_or_create(
        name='Jim', age=18, is_graduated=False, birthday=datetime.date(1998, 6, 6), college=college1
    )
    Student.objects.get_or_create(
        name='Bing', age=22, is_graduated=True, birthday=datetime.date(1994, 2, 6), college=college1
    )
    Student.objects.get_or_create(
        name='Monica', age=25, is_graduated=True, birthday=datetime.date(1991, 2, 6), college=college2
    )

    return Student.objects.extra(select={'is_young': 'birthday < "1995-07-06"'})


def create_college_and_get_queryset():
    college1, _ = College.objects.get_or_create(name="College 1st")
    college2, _ = College.objects.get_or_create(name="College 2nd")

    Student.objects.get_or_create(
        name='Jim', age=18, is_graduated=False, birthday=datetime.date(1998, 6, 6), college=college1
    )
    Student.objects.get_or_create(
        name='Bing', age=22, is_graduated=True, birthday=datetime.date(1994, 2, 6), college=college1
    )
    Student.objects.get_or_create(
        name='Monica', age=25, is_graduated=True, birthday=datetime.date(1991, 2, 6), college=college2
    )

    return College.objects.annotate(student_count=models.Count('students'))
