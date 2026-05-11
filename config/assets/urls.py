from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, DeviceViewSet, AssignmentViewSet, export_excel
from .views import device_page, dashboard, home, devices_list
from . import views
from django.contrib.auth import views as auth_views




router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'devices', DeviceViewSet)
router.register(r'assignments', AssignmentViewSet)

urlpatterns = [
    # Web views (avval)
    path('', home, name='home'),
    path('devices/', devices_list, name='devices_list'),
    path('device/<str:inventory_number>/', device_page, name='device_page'),
    path('dashboard/', dashboard, name='dashboard'),
    path('export/excel/', export_excel, name='export_excel'),
    
    # API routes (oxirida)
    path('', include(router.urls)),
    path('qr-print/', views.qr_print_page, name='qr_print'),
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),
    
]

