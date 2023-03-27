from django.urls import path, include
from rest_framework import routers

from .views import EmployeeViewSet


router = routers.DefaultRouter()
router.register(r'model-viewset', EmployeeViewSet) # newly registered ViewSet

urlpatterns = [
    path('employees-list', EmployeeViewSet.as_view({'get':'list'})),
    path('add-employee', EmployeeViewSet.as_view({'post':'create'})),
    path('delete-employee', EmployeeViewSet.as_view({'delete':'destroy'})),
    path('', include(router.urls)),
]