from rest_framework import generics
from employee.api.serializers import EmployeeSerializer
from rest_framework.permissions import IsAuthenticated
from employee.models import Employee
from employee.constants import LIST_RELATION_DISPLAY, CONTACTS, POSITIONS
from employee.decorators import rate_limit
from employee.pagination import CustomCursorPagination


class EmployeeListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    ordering = "-id"
    pagination_class = CustomCursorPagination # using Cursor Pagination for large data set

    def get_serializer(self, *args, **kwargs):
        fields_to_include = ['id', 'first_name', 'last_name', 'avatar', 'status']
    
        # logic here to determine the fields dynamically
        display_fields = self.request.user.organization.display_fields or []
        for field in display_fields:
            if field == POSITIONS.lower():
                fields_to_include += ['list_' + field]
            elif field in LIST_RELATION_DISPLAY:
                fields_to_include += [field]

        kwargs['fields_to_include'] = fields_to_include
        return super(EmployeeListView, self).get_serializer(*args, **kwargs)

    def get_queryset(self):
        query_set = super().get_queryset()
        filter_statuses = self.request.GET.getlist('status')
        filter_position_id = self.request.GET.get('position_id')
        filter_full_name = self.request.GET.get('full_name')
        filter_company_id = self.request.GET.get('company_id')
        filter_location_id = self.request.GET.get('location_id')
        filter_department_id = self.request.GET.get('department_id')

        organization = self.request.user.organization
        display_fields = organization.display_fields or []
        
        # handle filtering by full name
        if filter_full_name:
            split_names = filter_full_name.split(' ', 1)
            last_name = None
            if len(split_names) == 2:
                first_name, last_name = split_names
                query_set.filter(first_name__icontains=first_name, last_name__icontains=last_name)
            else:
                first_name = split_names[0]
                query_set = query_set.filter(first_name__icontains=first_name)
        
        if filter_statuses:
            query_set = query_set.filter(status__in=filter_statuses)
        
        if filter_position_id:
            query_set = query_set.filter(positions=filter_position_id)
        
        if filter_company_id:
            query_set = query_set.filter(company_id=filter_company_id)
        
        if filter_location_id:
            query_set = query_set.filter(location_id=filter_location_id)
        
        if filter_department_id:
            query_set = query_set.filter(department_id=filter_department_id)
        
        # useing select_related or prefrech_related to have better performance
        for field in display_fields:
            if field in LIST_RELATION_DISPLAY and field != CONTACTS.lower() and field != POSITIONS.lower():
                query_set = query_set.select_related(field)
            elif field == POSITIONS.lower():
                query_set = query_set.prefetch_related(field)

        # get employees belongs to user's organization
        query_set = query_set.filter(organization_id=organization.pk)
        return query_set
    
    @rate_limit
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
