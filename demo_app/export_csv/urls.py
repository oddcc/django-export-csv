from django.conf.urls import url
from export_csv import views


urlpatterns = (
    url(r'^$', views.StudentListView.as_view(), name='get_csv'),
)
