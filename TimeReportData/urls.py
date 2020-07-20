from django.conf.urls import url
from .views import FileView

urlpatterns = [
    url(r'^payroll/', FileView.as_view(), name='payroll-upload'),
]
