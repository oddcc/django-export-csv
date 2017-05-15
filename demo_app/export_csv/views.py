from django_export_csv.mixin import QueryCsvMixin
from django.views.generic.list import ListView

from .models import Student
from .data_init import create_student_and_get_queryset


def boolean_serializer(value):
    if value == True:
        return 'Y'
    else:
        return 'N'


class StudentListView(QueryCsvMixin, ListView):
    filename = 'export_student_list'
    add_datestamp = True
    use_verbose_names = True
    exclude_field = ['id']
    field_order = ['name', 'is_graduated']
    field_header_map = {'is_graduated': 'Graduated'}
    field_serializer_map = {'is_graduated': boolean_serializer}
    queryset = Student.objects.all()

    def get(self, *args, **kwargs):
        queryset = create_student_and_get_queryset()
        return self.render_csv_response(queryset)
