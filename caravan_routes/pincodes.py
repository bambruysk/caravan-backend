from rest_framework.response import Response

from .models import Pincode


def get_pincode_by_text(pincode_text: str) -> Pincode:
    try:
        pincode = Pincode.objects.get(text=pincode_text)
        return pincode
    except:
        return None


def get_pincode_user(pincode_text : str):
    return get_pincode_by_text(pincode_text).user


class PincodeNotFoundResponse(Response):
    def __init__(self, pincode=None):
        super().__init__({"error": "Pincode not found"}, status=403)


class PincodeIsUsedResponse(Response):
    def __init__(self, pincode=None):
        super().__init__()

