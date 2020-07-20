from django.contrib import admin
from .models import EmployeeTimeReportData, TimeReportFile, Employee

admin.site.register(Employee)
admin.site.register(EmployeeTimeReportData)
admin.site.register(TimeReportFile)
