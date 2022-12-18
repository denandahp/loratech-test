from django.forms.models import model_to_dict

from loratech_test.api.response import ErrorResponse

from rest_framework import request, status
from rest_framework.response import Response
from rest_framework.views import APIView

from loratech_test.api.users.forms import UserForm

class IndexUsers(APIView):

    def get(self, request: request) -> Response:
        form = GetShipmentOrderForm(data=request.data or None)
        if form.is_valid():
            order_dict = []
            orders, shipment_dict = form.save()
            for order in orders:
                order_dict.append({
                    'order_number': order.order_number,
                    'shipments': shipment_dict.get(order.order_number, '')
                })

            return Response(data={'orders': order_dict}, status=status.HTTP_200_OK)
        return ErrorResponse(form=form)

class CreateUsers(APIView):

    def post(self, request: request) -> Response:
        form = UserForm(data=request.data or None)
        if form.is_valid():
            user, balance, transaction_log = form.save()
            data ={
                'messages': f'Service {user} berhasil diupdate',
                'data': model_to_dict(user),
                'balace': model_to_dict(balance),
                'transaction': model_to_dict(transaction_log),
                'is_success': True
            }
            return Response(data=data, status=status.HTTP_200_OK)
        return ErrorResponse(form=form)