import factory
from employee.models import *
from employee.constants import ACTIVE
from users.models import Organization


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization

    name = factory.Faker('name')
    

class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    name = factory.Faker('name')
    
    
class LocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Location

    name = factory.Faker('name')
    
    
class DepartmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Department

    name = factory.Faker('name')
    

class PositionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Position

    name = factory.Faker('name')


class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Employee

    first_name = 'Hung'
    last_name = 'Nguyen Thanh'
    avatar = ''
    status = ACTIVE
    
    organization = factory.SubFactory(OrganizationFactory)
    location  = factory.SubFactory(LocationFactory)
    company = factory.SubFactory(CompanyFactory)
    department = factory.SubFactory(DepartmentFactory)
    