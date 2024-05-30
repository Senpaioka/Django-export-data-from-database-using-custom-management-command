from django.core.management.base import BaseCommand, CommandError
from main_site.models import StudentModel
import datetime
import csv

class Command(BaseCommand):

    help = 'Export data from student_model database'

    def handle(self, *args, **options):
        pass
        # database
        student_data = StudentModel.objects.all()

        # open file
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d')
        file_name = f'data_{timestamp}.csv'


        try:
            
            with open(file_name, 'w', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(['Roll No', 'Name', 'Age'])
            
                for data in student_data:
                    csv_writer.writerow([data.roll_no, data.name, data.age])
        
            self.stdout.write(self.style.SUCCESS('Data Export Completed !!'))

        except:

            self.stderr.write("Something Went Wrong")


# example how to use:
# py manage.py exportdata 