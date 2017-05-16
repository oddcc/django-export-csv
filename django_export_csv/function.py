import datetime
import unicodecsv as csv
import codecs

from django.core.exceptions import ValidationError
from django.http import StreamingHttpResponse


class _Echo(object):
    """
    An file-like object that implements just the write method.
    """

    def write(self, value):
        return value


def render_csv_response(queryset, filename=None, add_datestamp=False, **kwargs):
    """
    entry function, making a CSV streaming http response, take a queryset
    """
    if filename:
        filename = _clean_filename(filename)
        if add_datestamp:
            filename = _add_datestamp(filename)
    else:
        filename = _generate_filename(queryset, add_datestamp)

    response_args = {'content_type': 'text/csv'}

    response = StreamingHttpResponse(
        _iter_csv(queryset, _Echo(), **kwargs), **response_args)

    # support chinese filename
    response['Content-Disposition'] = b'attachment; filename=%s;' % filename.encode(encoding='utf-8')
    response['Cache-Control'] = 'no-cache'

    return response


def _clean_filename(filename):
    if '.' in filename:
        if not filename.endswith('.csv'):
            raise ValidationError('file extension should be .csv')
    else:
        filename = "%s.csv" % filename
    return filename


def _add_datestamp(filename):
    if filename != _clean_filename(filename):
        raise ValidationError('filename must be cleaned first')

    date_string = datetime.date.today().strftime("%Y%m%d")
    return '%s_%s.csv' % (filename[:-4], date_string)


def _generate_filename(queryset, add_datestamp):
    filename = queryset.model._meta.model_name
    filename = _clean_filename(filename)
    if add_datestamp:
        filename = _add_datestamp(filename)
    return filename


def _iter_csv(queryset, file_obj, **kwargs):
    """
    Writes CSV data to a file object based on the
    contents of the queryset and yields each row.
    """
    csv_kwargs = {'encoding': 'utf-8'}

    # add BOM to support MS Excel (for Windows only)
    yield file_obj.write(codecs.BOM_UTF8)

    if type(queryset).__name__ == 'ValuesQuerySet':
        queryset_values = queryset
    else:
        queryset_values = queryset.values()

    field_names = [
        field_name
        for field_name in queryset_values.field_names
        if field_name not in kwargs.get('exclude_field', [])
    ]

    field_order = kwargs.get('field_order', [])

    if field_order:
        field_names = [field_name for field_name in field_names if field_name in field_order] + \
                      [field_name for field_name in field_names if field_name not in field_order]

    writer = csv.DictWriter(file_obj, field_names, **csv_kwargs)

    header_map = dict((field, field) for field in field_names)

    use_verbose_names = kwargs.get('use_verbose_names', True)

    if use_verbose_names:
        header_map.update(
            dict((field.name, field.verbose_name)
                 for field in queryset.model._meta.fields
                 if field.name in field_names))

    header_map.update(kwargs.get('field_header_map', {}))

    yield writer.writerow(header_map)

    for item in queryset_values:
        item = _sanitize_item(item, **kwargs)
        yield writer.writerow(item)


def _sanitize_item(item, field_serializer_map={}, **kwargs):
    def _serialize_value(value):
        if isinstance(value, datetime.datetime):
            return value.isoformat()
        else:
            return str(value)

    obj = {}
    for key, val in item.items():
        if key in kwargs.get('exclude_field', []):
            continue
        if val is not None:
            serializer = field_serializer_map.get(key, _serialize_value)
            newval = serializer(val)
            if not isinstance(newval, str):
                newval = str(newval)
            obj[key] = newval
    return obj
