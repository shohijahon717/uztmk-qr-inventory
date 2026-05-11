import qrcode

from io import BytesIO

from django.core.files import File


def generate_qr(device):

    url = f"http://127.0.0.1:8000/device/{device.inventory_number}/"

    qr = qrcode.make(url)

    buffer = BytesIO()

    qr.save(buffer, format='PNG')

    filename = f"{device.inventory_number}.png"

    device.qr_code.save(
        filename,
        File(buffer),
        save=False
    )