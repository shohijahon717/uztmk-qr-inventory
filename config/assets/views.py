from rest_framework import viewsets
from .models import Employee, Device, Assignment
from .serializers import EmployeeSerializer, DeviceSerializer, AssignmentSerializer
from .services import generate_qr
from django.shortcuts import get_object_or_404, render
from .models import Assignment
from rest_framework import viewsets, filters
from django.http import HttpResponse
from openpyxl import Workbook
from .models import Assignment
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required


@login_required
def qr_print_page(request):

    ids = request.GET.get('ids')

    if not ids:
        return HttpResponse("Qurilmalar tanlanmagan")

    id_list = ids.split(',')

    devices = Device.objects.filter(id__in=id_list)

    return render(request, 'qr_print.html', {
        'devices': devices
    })

def home(request):
    """Bosh sahifa"""
    return render(request, 'index.html')

@login_required
def devices_list(request):
    """Barcha qurilmalarni ko'rsatadigan sahifa"""
    return render(request, 'devices.html')

@login_required
def dashboard(request):
    assignments = Assignment.objects.filter(
        is_active=True
    ).select_related(
        'device',
        'employee'
    ).order_by('-id')
    total_devices = Device.objects.count()
    assigned_devices = Device.objects.filter(status='assigned').count()
    available_devices = Device.objects.filter(status='warehouse').count()
    total_employees = Employee.objects.count()
    available_devices = Device.objects.filter(status='warehouse')

    available_devices_count = available_devices.count()

    return render(request, 'dashboard.html', {
        'available_devices': available_devices,
        'assignments': assignments,
        'total_devices': total_devices,
        'assigned_devices': assigned_devices,
        'available_devices': available_devices,
        'available_devices_count': available_devices_count,
        'total_employees': total_employees,
    })


def device_page(request, inventory_number):
    device = get_object_or_404(Device, inventory_number=inventory_number)

    # 👇 ENG MUHIM QISM
    #assignment = Assignment.objects.filter(device=device).last()
    assignment = Assignment.objects.filter(
        device=device,
        is_active=True
    ).last()

    return render(request, 'device.html', {
        'device': device,
        'assignment': assignment,
    })


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class DeviceViewSet(viewsets.ModelViewSet):

    queryset = Device.objects.all().order_by('-id')

    serializer_class = DeviceSerializer

    def perform_create(self, serializer):

        device = serializer.save()

        generate_qr(device)

        device.save()

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    # 👇 QIDIRUV
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'device__inventory_number',
        'employee__tabel_number',
        'employee__full_name'
    ]

    @action(detail=True, methods=['post'])

    def return_device(self, request, pk=None):

        assignment = self.get_object()

        device = assignment.device

        device.status = 'warehouse'

        device.save()
        assignment.is_active = False
        assignment.save()

        return Response({
            'message': 'Qurilma qaytarildi'
        })

@login_required
def export_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Assignments"

    # Header
    ws.append([
        "Inventar raqam",
        "Qurilma nomi",
        "Serial raqam",
        "Xodim F.I.O",
        "Tabel raqami",
        "Bo‘lim",
        "Topshirilgan sana",
        "Izoh"
    ])

    assignments = Assignment.objects.select_related('device', 'employee')

    for a in assignments:
        ws.append([
            a.device.inventory_number,
            a.device.name,
            a.device.serial_number,
            a.employee.full_name,
            a.employee.tabel_number,
            a.employee.department,
            str(a.assigned_at),
            a.note
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=assignments.xlsx'

    wb.save(response)
    return response
