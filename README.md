# PayrollSystemAPI
API to upload a CSV file containing data on the number of hours worked per day per employee and retrieve a report detailing how much each employee should be paid in each pay period

## Instructions on how to build/run the application
1. create a directory : mkdir project_name
1. go to that directory : cd project_name
1. unbundle the code
1. install the required packages with the given command on command prompt:  pip install -r requirements.txt
1. run these commands:
    1. python manage.py makemigrations
    1. python manage.py migrate
    1. python manage.py createsuperuser
    1. python manage.py runserver
1. use given url for end point to upload time report and to retrieve the payroll report
      http://127.0.0.1:8000/payroll/
      

### How did you test that your implementation was correct?
I have tested the post and get method of the API using Postman online. I have tested uploading files with different set of data and retrieving the required information.
I have also tested uploading file with same report ID that was previously uploaded for throwing appropriate error.

### If this application was destined for a production environment, what would you add or change?
1. Set DEBUG to False in settings.py sensitive/confidential debug trace and variable information from being displayed)
1. Change setting of SECRECT_KEY so that the key used in production is not in source control or accessible outside the production server. Key can be read from environment variable or from a file.
1. Change the DATABASES configuration in settings.py as default sqllite3 is not recommended for Production.

### What compromises did you have to make as a result of the time constraints of this challenge?
Few of the personal planned items were impacted but no regrets on that. I made sure my office work is not impacted with this challenge. 
