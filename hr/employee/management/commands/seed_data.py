from django.core.management.base import BaseCommand
from employee.models import  *
from users.models import *
from employee.constants import ACTIVE, COMPANY, DEPARTMENT
from django.db import transaction


class Command(BaseCommand):
    """
    Command that used to seeding data
    Command: python manage.py seed_data 
    """
    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                location, _ = Location.objects.get_or_create(name='Signapore')
                department, _ = Department.objects.get_or_create(name='Department 1')
                company, _ = Company.objects.get_or_create(name='Company 1')
                organization, _ =  Organization.objects.get_or_create(
                    name='Organization A', display_fields=[COMPANY.lower(), DEPARTMENT.lower()]
                )
                position, _ = Position.objects.get_or_create(name='Back-end')
                
                list_employees = []
                for id in range(10):
                    list_employees.append(Employee(
                        first_name=f'Employee {id}',
                        last_name='Employee',
                        avatar='avatar',
                        status=ACTIVE,
                        organization=organization,
                        company=company,
                        department=department,
                        location=location,
                    ))
                Employee.objects.bulk_create(list_employees)
                for employee in Employee.objects.all():
                    employee.positions.set([position])
                
                self.stdout.write("Seed data successfully")
                
        except Exception as e:
            self.stdout.write(f"Errors: {str(e)}")

        self.stdout.write("Run command successfully")
        