from django.conf.urls import url
from . import views


urlpatterns = (
    url(r'^$', views.StudentListView.as_view()),
    url(r'^function$', views.student_list_view),
)