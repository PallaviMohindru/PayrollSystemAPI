from rest_framework import serializers
from .models import EmployeeTimeReportData, TimeReportFile

class EmployeeTimeReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeTimeReportData
        fields = ("date", "hours_worked", "employee", "job_group")


class TimeReportFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeReportFile
        fields = ("file", "file_name", "uploaded_on")
