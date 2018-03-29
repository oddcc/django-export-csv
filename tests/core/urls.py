from __future__ import unicode_literals
from __future__ import absolute_import
from django.conf.urls import url

from tests.core import views

urlpatterns = [
    url(r'^$', views.StudentListView.as_view()),
    url(r'^college$', views.CollegeListView.as_view()),
    url(r'^function$', views.student_list_view),
]
