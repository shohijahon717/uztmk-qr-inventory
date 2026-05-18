from django.db import models
from django.core.exceptions import ValidationError

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
        max_length=20,
        unique=True,
        blank=True
    )

    name = models.CharField(max_length=255)

    serial_number = models.CharField(
        max_length=255
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='warehouse'
    )

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

            # Eski inventar berilgan bo'lsa
            if self.old_inventory_number:

                normalized = (
                    self.old_inventory_number.strip()
                )

                # 1222 → 001222
                if normalized.isdigit():
                    normalized = normalized.zfill(6)

                # Takrorligini tekshirish
                if Device.objects.filter(
                    inventory_number=normalized
                ).exists():

                    raise ValidationError(
                        f"{normalized} inventar allaqachon mavjud"
                    )

                self.inventory_number = normalized

            else:

                # Faqat 6 xonali avto inventarlarni olish
                auto_devices = Device.objects.filter(
                    inventory_number__regex=r'^\d{6}$'
                )

                if auto_devices.exists():

                    last_number = max(
                        int(device.inventory_number)
                        for device in auto_devices
                    )

                    new_number = last_number + 1

                else:

                    new_number = 1

                self.inventory_number = (
                    str(new_number).zfill(6)
                )

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