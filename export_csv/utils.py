import datetime

from django.core.exceptions import ValidationError


def clean_filename(filename):
    if '.' in filename:
        if not filename.endswith('.csv'):
            raise ValidationError('file extension should be .csv')
    else:
        filename = "%s.csv" % filename
    return filename


def attach_datestamp(filename):
    if filename != clean_filename(filename):
        raise ValidationError('filename must be cleaned first')

    date_string = datetime.date.today().strftime("%Y%m%d")
    return '%s_%s.csv' % (filename[:-4], date_string)


def generate_filename(queryset, add_datestamp=False):
    filename = queryset.model._meta.model_name
    filename = clean_filename(filename)
    if add_datestamp:
        filename = attach_datestamp(filename)
    return filename


def get_uncontain_field_names(list1, list2):
    return [i for i in list1 if i not in list2]


class Echo(object):
    """
    An file-like object that implements just the write method.
    """

    def write(self, value):
        return value
