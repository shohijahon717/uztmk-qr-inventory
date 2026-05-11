from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, DeviceViewSet, AssignmentViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'devices', DeviceViewSet)
router.register(r'assignments', AssignmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]   