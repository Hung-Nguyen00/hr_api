from django.db import models
from employee.constants import EMPLOYEE_ACTIVE_STATUS
from model_utils.models import TimeStampedModel
from users.models import Organization

class Location(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self) -> str:
        return self.name
    
    
class Department(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self) -> str:
        return self.name


class Company(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name
    

class Position(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Employee(TimeStampedModel):
    first_name = models.CharField(max_length=50, db_index=True)
    last_name = models.CharField(max_length=50)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, choices=EMPLOYEE_ACTIVE_STATUS)
    contacts = models.JSONField(default=dict)
    personal_email = models.EmailField(blank=True, null=True)
    
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, blank=True, null=True)
    positions = models.ManyToManyField(Position, related_name='employees')
    
    def __str__(self) -> str:
        return self.first_name
    
    @property
    def company_name(self):
        return self.company.name if self.company else 'No company'
    
    @property
    def location_name(self):
        return self.location.name if self.location else 'No location'

    @property
    def department_name(self):
        return self.department.name if self.department else 'No department'
    
    @property
    def list_positions(self):
        if self.positions.all():
            return [position.name for position in self.positions.all()]
        return []
    