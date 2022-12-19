import json

from typing import Optional

from django.forms import Form

from rest_framework import status
from rest_framework.response import Response


class ErrorResponse(Response):
    """
    API subclass from rest_framework response to simplify constructing error messages
    """
    def __init__(self, form: Optional[Form] = None, error_code: str = "", error_message: str = ""):
        super().__init__(status=status.HTTP_400_BAD_REQUEST)

        data: dict = {
            'error_message': 'Your request cannot be completed',
            'error_code': 'invalid_request'
        }

        if error_code:
            data["error_code"] = error_code

        if error_message:
            data["error_message"] = error_message

        if form and form.errors.items():
            data['errors'] = {}

            for field, errors in json.loads(form.errors.as_json()).items():
                key = field
                message = errors[0]['message']
                data['errors'][key] = message
                data["error_code"] = errors[0].get('code') if errors[0].get('code') else "invalid_data"
                data["error_message"] = message

                break
        self.data = data

def error_response(message: str) -> Response:
    data ={
        'messages': message,
        'is_success': False
    }
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
