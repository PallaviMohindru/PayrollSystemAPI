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
