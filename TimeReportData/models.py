from django.db import models
from django.utils.timezone import now


class Employee(models.Model):
    employee_id = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.employee_id)


# to store time report data from file
class EmployeeTimeReportData(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE
    )  # one employee can have many records
    date = models.DateField()
    hours_worked = models.FloatField(default=0)
    job_group = models.CharField(max_length=1, blank=True)
    created_on = models.DateTimeField(default=now, blank=True)

    def __str__(self):
        return str(self.employee.employee_id)


class TimeReportFile(models.Model):
    file = models.FileField()
    file_name = models.CharField(
        unique=True, max_length=200
    )  # this should be unique so that file with same file name could not be uploaded
    uploaded_on = models.DateTimeField(default=now, blank=True)

    def __str__(self):
        return self.file_name
