from rest_framework.test import APITestCase
from users.models import User
from django.urls import reverse
from employee.constants import RateLimitConfig
from django.core.cache import cache
from employee.factories import EmployeeFactory
from employee.constants import ACTIVE, TERMINATED, DEPARTMENT, CONTACTS, LIST_RELATION_DISPLAY


class YourAppTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='123321',
            email='test@gmail.com',
        )

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token.key}')
        self.first_employee = EmployeeFactory(
            organization_id=self.user.organization_id
        )
        self.second_employee = EmployeeFactory(first_name='test')

    def test_get_employee_success(self):
        cache.clear()
        url = reverse('employees_list')
        request = self.client.get(url)
        assert request.status_code == 200
        
    def test_get_employee_rate_limit(self):
        url = reverse('employees_list')
        for idx in range(1, RateLimitConfig.LIMIT):
            request = self.client.get(url)
            if idx == RateLimitConfig.LIMIT:
                assert request.status_code == 403
    
    def test_get_employee_filter_fullname(self):
        cache.clear()
        full_name = self.first_employee.first_name + ' ' + self.first_employee.last_name
        url = reverse('employees_list') + f'?full_name={full_name}'
        request = self.client.get(url)

        assert len(request.json()) == 1 

    def test_get_employee_filter_statuses(self):
        cache.clear()
        self.second_employee.status = TERMINATED
        self.second_employee.organization_id = self.user.organization_id
        self.second_employee.save()
        
        url = reverse('employees_list') + f'?status={ACTIVE}&status={TERMINATED}'
        request = self.client.get(url)

        assert len(request.json()) == 2
    
    def test_get_employee_filter_by_company_location_department(self):
        cache.clear()
        department_id = self.first_employee.department_id
        location_id = self.first_employee.location_id
        company_id = self.first_employee.company_id

        query_params = f'?department_id={department_id}&location_id={location_id}&compnay_id={company_id}'
        url = reverse('employees_list') + query_params
        request = self.client.get(url)
        assert len(request.json()) == 1
        
    def test_get_employee_filter_show_fields_from_configuration(self):
        cache.clear()
        organization = self.user.organization
        organization.display_fields = [DEPARTMENT.lower(), CONTACTS.lower()]
        organization.save()

        not_existing = list(set(LIST_RELATION_DISPLAY) -  set(organization.display_fields))
        url = reverse('employees_list')
        request = self.client.get(url)
        assert len(request.json()) == 1
        data = request.json()[0]
        for field in not_existing:
            assert field not in data.keys()

        