from rest_framework import serializers
from .models import Employee, Device, Assignment
from .services import generate_qr


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class AssignmentSerializer(serializers.ModelSerializer):
    tabel_number = serializers.CharField(write_only=True)
    full_name = serializers.CharField(write_only=True)
    department = serializers.CharField(write_only=True)
    device_info = serializers.SerializerMethodField()

    employee = serializers.SerializerMethodField()
    assigned_at = serializers.DateField(read_only=True)

    class Meta:
        model = Assignment
        fields = [
            'id',
            'device',
            'device_info',   # 👈 yangi
            'employee',
            'assigned_at',
            'tabel_number',
            'full_name',
            'department',
            'note'
        ]


    def get_device_info(self, obj):
        return {
            "inventory_number": obj.device.inventory_number,
            "name": obj.device.name,
            "serial_number": obj.device.serial_number
    }

    def get_employee(self, obj):
        return {
            "tabel_number": obj.employee.tabel_number,
            "full_name": obj.employee.full_name,
            "department": obj.employee.department
        }
    def create(self, validated_data):
        tabel = validated_data.pop('tabel_number')
        full_name = validated_data.pop('full_name')
        department = validated_data.pop('department')
        device = validated_data['device']

        if device.status == 'assigned':
            raise serializers.ValidationError("Device already assigned")

        employee, created = Employee.objects.get_or_create(
            tabel_number=tabel,
            defaults={
                "full_name": full_name,
                "department": department
            }
        )

        if not created:
            employee.full_name = full_name
            employee.department = department
            employee.save()

        device.status = 'assigned'
        device.save()

        assignment = Assignment.objects.create(
            device=device,
            employee=employee,
            note=validated_data.get('note', '')
        )

    # 👇 SHU YERDA ISHLATILADI
      

        return assignment
