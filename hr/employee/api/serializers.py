from rest_framework import serializers
from employee.models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    department = serializers.CharField(read_only=True)
    company = serializers.CharField(read_only=True)
    location = serializers.CharField(read_only=True)
    list_positions = serializers.ListField(read_only=True)
    
    class Meta:
        model = Employee
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        fields_to_include = kwargs.pop('fields_to_include', None)
        super(EmployeeSerializer, self).__init__(*args, **kwargs)

        if fields_to_include:
            # Dynamically set the fields based on fields_to_include
            self.fields = {field: self.fields[field] for field in fields_to_include}
            
    def get_department(self):
        return self.department_name
    
    def get_location(self):
        return self.location_name
    
    def get_company(self):
        return self.company_name
    
    def get_list_positions(self):
        return self.list_positions
