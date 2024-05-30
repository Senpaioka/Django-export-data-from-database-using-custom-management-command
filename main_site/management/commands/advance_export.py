from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
import datetime
import csv



class Command(BaseCommand):

    help = "Export data from selected database -- provide model name."

    # passing model name
    def add_arguments(self, parser):
        parser.add_argument("--model_name", type=str, help="Pass the model name")


    def handle(self, *args, **options):
        
        # get the database
        provided_model = options['model_name'].capitalize()

        found_model = None
        
        for app_data in apps.get_app_configs():
            try:
                found_model = apps.get_model(app_data.label, provided_model)
                break
            except LookupError:
                continue



        # open file
        file_creation_time = datetime.datetime.now().strftime('%Y-%m-%d')
        file_name = f'data_from_{provided_model}_{file_creation_time}.csv'

        if found_model is not None:
            data_queryset = found_model.objects.all()
            with open(file_name, 'w', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow([column_name.name for column_name in found_model._meta.get_fields()])

                for data in data_queryset:
                    csv_writer.writerow([getattr(data, value.name) for value in found_model._meta.fields])
            
            self.stdout.write(self.style.SUCCESS("Data Export Completed !!"))

        else :
            self.stderr.write("Provided Model Not Found !!")

        
        # Example how to use :
        # py manage.py advance_export --model_name StudentModel
    