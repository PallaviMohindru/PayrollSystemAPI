# PayrollSystemAPI
API to upload a CSV file containing data on the number of hours worked per day per employee and retrieve a report detailing how much each employee should be paid in each pay period

## Instructions on how to build and run the application
1. unbundle the code
1. install the required packages:  pip install -r requirements.txt
1. run these commands:
    1. python manage.py migrate
    1. python manage.py createsuperuser
    1. python manage.py runserver
1. use given url for end point to upload time report and to retrieve the payroll report
      http://127.0.0.1:8000/payroll/
