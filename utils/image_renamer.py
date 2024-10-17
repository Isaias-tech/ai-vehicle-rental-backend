from django.utils.crypto import get_random_string
from django.forms import ValidationError


def wrapper(instance, filename):
    ext = filename.split(".")[-1].lower()

    if ext not in ["jpg", "png", "jpeg"]:
        raise ValidationError(f"invalid image extension: {filename}")

    filename = f"profile_pictures/{get_random_string(50)}.{ext}"
    return filename
