from django.urls import path
from rest_framework.routers import DefaultRouter
from employee.api.views import EmployeeListView

router = DefaultRouter()

urlpatterns = [
    path('', EmployeeListView.as_view(), name='employees_list')
] + router.urls