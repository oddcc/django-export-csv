# django-export-csv
## Introduction
Django的一个CSV导出工具
可以很方便的把queryset导出为CSV文件, 为了避免导出文件过大, 占用服务器内存, 生成的是StreamingHttpResponset.

支持通过下面几种方式对导出的CSV文件进行定制
1. 文件名
2. 导出的时候文件名加/不加时间戳
3. 表头是不是使用verbose_name
4. 可以排除不想导出的字段
5. 自定义导出字段的顺序
6. 自定义表头
7. 自定义字段的表现形式(serializer)
8. 支持导出外键, 多对多, 外键反向查询这些关系, 需要自定义

## install
Run:
```
pip install django-export-csv
```
Support Python 2.7 and 3.5, Django >= 1.8.

## usage
使用CBV的话, 视图类需要继承`ListView`(或`MultipleObjectMixin`的子类)和`QueryCsvMixin`, 继承之后就可以调用`render_csv_response`方法把queryset导出为CSV文件, `render_csv_response`方法需要一个`QuerySet`或`ValuesQuerySet`的实例作为参数:

### 使用CBV
```python
from django_export_csv import QueryCsvMixin
from django.views.generic.list import ListView

from .models import Student


class StudentListView(QueryCsvMixin, ListView):
    queryset = Student.objects.all()

    def get(self, *args, **kwargs):
        return self.render_csv_response(queryset)
```

### 使用FBV
```python
from django_export_csv import render_csv_response


def student_list_view(request):
    if request.method == 'GET':
        queryset = Student.objects.all()
        return render_csv_response(queryset)
```

## 定制 CSV
视图类继承了 `QueryCsvMixin`之后, 就可以使用以下参数自定义CSV文件:
1. `filename` - (default: `None`), 是个字符串, 如果不定义, CSV会根据model来生成文件名.
2. `add_datestamp` - (default: `False`), 是个布尔值, 如果为True的话, 导出的文件名末尾会添加当前时间的时间戳.
3. `use_verbose_names` - (default: `True`), 是个布尔值, 如果设为True, CSV表头的名称会使用model中定义的verbose_name.
4. `exclude_field` - (default: `[]`), 是个包含了不想导出的字段名的列表, 不设的话, 默认导出所有字段.
5. `field_order` - (default: `[]`), 是个列表, 可以把想定义排序的字段名写在里面, 导出的CSV会优先按顺序排列这个参数指定的字段, 再排剩下的字段.
6. `field_header_map` - (default: `{}`), 是个字典, 用于自定义表头, key应该是字段名, value是表头中显示的内容, 这个参数的优先级比verbose_name高.
7. `field_serializer_map` - (default: `{}`), 是个字典, 用于自定义serializer, key是字段名, value是对应的函数名, 这个函数应该接收一个值并返回相应的内容.
8. `extra_field` - (default: `[]`), 是个列表, 用于定义不在数据库表中但又与model相关的字段, 比如外键的反向查询, 多对多关系等等, 也可以用于定义任意字段. 注意如果指定了`extra_field`参数, `field_serializer_map`中必须有相应的serializer配合才能工作.

e.g:

```python
# data_init.py
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

```

```python
# views.py
from django_export_csv import QueryCsvMixin
from django_export_csv import render_csv_response
from django.views.generic.list import ListView

from .models import Student
from .data_init import create_student_and_get_queryset


def boolean_serializer(value):
    if value == True:
        return 'Y'
    else:
        return 'N'
        
        
def college_serializer(obj):
    return obj.college.name


# CBV
class StudentListView(QueryCsvMixin, ListView):
    filename = 'export_student_list'
    add_datestamp = True
    use_verbose_names = True
    exclude_field = ['id']
    field_order = ['name', 'is_graduated']
    field_header_map = {'is_graduated': 'Graduated'}
    field_serializer_map = {'is_graduated': boolean_serializer, 'college': college_serializer}
    queryset = Student.objects.all()
    extra_field = ['college']

    def get(self, *args, **kwargs):
        queryset = create_student_and_get_queryset()
        return self.render_csv_response(queryset)
        

# FBV
def student_list_view(request):
    filename = 'export_student_list'
    add_datestamp = True
    use_verbose_names = True
    exclude_field = ['id']
    field_order = ['name', 'is_graduated']
    field_header_map = {'is_graduated': 'Graduated'}
    field_serializer_map = {'is_graduated': boolean_serializer, 'college': college_serializer}
    extra_field = ['college']

    if request.method == 'GET':
        queryset = create_student_and_get_queryset()
        return render_csv_response(
            queryset, filename=filename, add_datestamp=add_datestamp, use_verbose_names=use_verbose_names,
            exclude_field=exclude_field, field_order=field_order, field_header_map=field_header_map,
            field_serializer_map=field_serializer_map, extra_field=extra_field
        )
```
