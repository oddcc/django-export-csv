from django_export_csv.mixin import QueryCsvMixin
from django.views.generic.list import ListView

from .models import Student
from .data_init import create_student_and_get_queryset


class StudentListView(QueryCsvMixin, ListView):
    queryset = Student.objects.all()

    def get(self, *args, **kwargs):
        queryset = create_student_and_get_queryset()
        return self.render_csv_response(queryset)