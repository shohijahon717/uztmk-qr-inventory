from django.db import models

class Employee(models.Model):
    tabel_number = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name


class Device(models.Model):
    STATUS_CHOICES = [
        ('warehouse', 'Omborda'),
        ('assigned', 'Berilgan'),
    ]
   

    inventory_number = models.CharField(
    max_length=6,
    unique=True,
    blank=True
    )
    name = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='warehouse')
    qr_code = models.ImageField(
    upload_to='qr_codes/',
    blank=True,
    null=True
    )
    description = models.TextField(
        blank=True,
        null=True
    )
    old_inventory_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    def save(self, *args, **kwargs):

        if not self.inventory_number:

            last_device = Device.objects.order_by('-id').first()

            if last_device and last_device.inventory_number.isdigit():

                new_number = int(last_device.inventory_number) + 1

            else:

                new_number = 1

            self.inventory_number = str(new_number).zfill(6)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.inventory_number


class Assignment(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    assigned_at = models.DateField(auto_now_add=True)
    note = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)