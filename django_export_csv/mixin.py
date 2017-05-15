# -*- coding: utf-8 -*-
import datetime
import unicodecsv as csv
import codecs

from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.http import StreamingHttpResponse


class QueryCsvMixin(object):
    filename = None
    add_datestamp = False
    use_verbose_names = True
    exclude_field = []
    field_order = []
    field_header_map = {}
    field_serializer_map = {}

    class Echo(object):
        def write(self, value):
            return value

    def render_csv_response(self, queryset):
        if self.filename:
            filename = self._clean_filename(self.filename)
            if self.add_datestamp:
                filename = self._add_datestamp(filename)
        else:
            filename = self._generate_filename()

        response_args = {'content_type': 'text/csv'}

        response = StreamingHttpResponse(
            self._iter_csv(queryset, self.Echo()), **response_args)

        response['Content-Disposition'] = 'attachment; filename=%s;' % filename
        response['Cache-Control'] = 'no-cache'

        return response

    def _clean_filename(self, filename):
        if '.' in filename:
            if not filename.endswith('.csv'):
                raise ValidationError('file extension should be .csv')
        else:
            filename = "{}.csv".format(filename)
        return filename

    def _add_datestamp(self, filename):
        if filename != self._clean_filename(filename):
            raise ValidationError('filename must be cleaned first')

        date_string = datetime.date.today().strftime("%Y%m%d")
        return '%s_%s.csv' % (filename[:-4], date_string)

    def _generate_filename(self):
        queryset = self.get_queryset()
        filename = queryset.model._meta.model_name
        filename = self._clean_filename(filename)
        if self.add_datestamp:
            filename = self._add_datestamp(filename)
        return filename

    def _iter_csv(self, queryset, file_obj, **kwargs):
        csv_kwargs = {'encoding': 'utf-8'}

        yield file_obj.write(codecs.BOM_UTF8)

        if type(queryset).__name__ == 'ValuesQuerySet':
            queryset_values = queryset
        else:
            queryset_values = queryset.values()

        field_names = [
            field_name
            for field_name in queryset_values.field_names
            if field_name not in self.exclude_field
        ]

        field_names = [field_name for field_name in field_names if field_name in self.field_order] + \
                      [field_name for field_name in field_names if field_name not in self.field_order]

        writer = csv.DictWriter(file_obj, field_names, **csv_kwargs)

        header_map = dict((field, field) for field in field_names)
        if self.use_verbose_names:
            header_map.update(
                dict((field.name, field.verbose_name)
                     for field in queryset.model._meta.fields
                     if field.name in field_names))
        header_map.update(self.field_header_map)

        yield writer.writerow(header_map)

        for item in queryset_values:
            item = self._sanitize_item(self.field_serializer_map, item)
            yield writer.writerow(item)

    def _sanitize_item(self, field_serializer_map, item):
        def _serialize_value(value):
            if isinstance(value, datetime.datetime):
                return value.isoformat()
            else:
                return str(value)

        obj = {}
        for key, val in item.items():
            if key in self.exclude_field:
                continue
            if val is not None:
                serializer = field_serializer_map.get(key, _serialize_value)
                newval = serializer(val)
                if not isinstance(newval, str):
                    newval = str(newval)
                obj[key] = newval
        return obj
