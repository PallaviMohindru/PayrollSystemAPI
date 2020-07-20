from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TimeReportFileSerializer, EmployeeTimeReportSerializer
from .models import EmployeeTimeReportData, Employee
from os import read
import csv, io
import datetime
import calendar


class FileView(APIView):

    def post(self, request, *args, **kwargs):
        csv_file = request.FILES["file"]
        data_set = csv_file.read().decode("utf-8")
        io_string = io.StringIO(data_set)
        file_serializer = TimeReportFileSerializer(
            data={"file": csv_file, "file_name": csv_file.name}
        )

        # saving file in db
        if file_serializer.is_valid():
            file_serializer.save()
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        next(io_string) # skip header row
        for column in csv.reader(io_string, delimiter=","):
            employee_id = column[2]
            employee_obj, created = Employee.objects.get_or_create(
                employee_id=employee_id
            )
            date = column[0]
            format_str = "%d/%m/%Y"  # The format
            datetime_obj = datetime.datetime.strptime(date, format_str)
            time_report_data = {
                "employee": employee_obj.pk,
                "date": datetime_obj.date(),
                "hours_worked": column[1],
                "job_group": column[3],
            }
            time_report_serializer = EmployeeTimeReportSerializer(data=time_report_data)

            # saving data from file in db
            if time_report_serializer.is_valid():
                time_report_serializer.save()

            else:
                return Response(
                    time_report_serializer.errors, status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(file_serializer.data, status=status.HTTP_200_OK)


    def get(self, request, *args, **kwargs):
        dates = EmployeeTimeReportData.objects.all().order_by("date")
        min_date = dates.first().date
        max_date = dates.last().date
        employee_reports = []
        while min_date < max_date: #data sorted by dates
            if min_date.day < 16:
                pay_start_date = min_date.replace(day=1)
                pay_end_date = pay_start_date + datetime.timedelta(days=14)
            else:
                pay_start_date = min_date.replace(day=16)
                last_day_of_month = calendar.monthrange(
                    pay_start_date.year, pay_start_date.month
                )[1]
                pay_end_date = pay_start_date.replace(day=last_day_of_month)

            employees = Employee.objects.all()

            for employee in employees:
                data = {}
                employee_time_report_data = EmployeeTimeReportData.objects.filter(
                    date__range=[pay_start_date, pay_end_date], employee=employee
                )

                #houly rate calculation based on Job group
                for record in employee_time_report_data:
                    if record.job_group == "A":
                        amountPaid = record.hours_worked * 20
                    elif record.job_group == "B":
                        amountPaid = record.hours_worked * 30

                    data = {
                        "employeeId": employee.employee_id,
                        "payPeriod": {
                            "startDate": pay_start_date,
                            "endDate": pay_end_date,
                        },
                        "amountPaid": "${}".format(str(amountPaid)),
                    }
                    employee_reports.append(data)

            min_date = pay_end_date + datetime.timedelta(1)

        result = {"payrollReport": {"employeeReports": employee_reports}}
        return Response(result)
