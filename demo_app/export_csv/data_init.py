import datetime
from .models import Student, College


def create_student_and_get_queryset():
    college1, _ = College.objects.get_or_create(name="College 1st")
    college2, _ = College.objects.get_or_create(name="College 2nd")

    Student.objects.get_or_create(
        name='Jim', age=18, is_graduated=False, birthday=datetime.date(1998,6,6), college=college1
    )
    Student.objects.get_or_create(
        name='Bing', age=22, is_graduated=True, birthday=datetime.date(1994, 2, 6), college=college1
    )
    Student.objects.get_or_create(
        name='Monica', age=25, is_graduated=True, birthday=datetime.date(1991, 2, 6), college=college2
    )

    return Student.objects.all()
