from django.urls import include, path

urlpatterns = [
    path("employee/", include("employee.api.urls")),    
]