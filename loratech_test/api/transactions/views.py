from django.forms.models import model_to_dict

from loratech_test.api.response import ErrorResponse

from rest_framework import request, status
from rest_framework.response import Response
from rest_framework.views import APIView

from loratech_test.api.transactions.forms import DepositForm, WithdrawForm
from loratech_test.apps.transactions.model import TransactionLog
from loratech_test.apps.users.model import User

class Deposit(APIView):
    '''
    Payload:
        {
            "user_id": 1,
            "amount": 2000
        }
    Response:
    {
        "messages": "Proses deposit berhasil",
        "is_success": true,
        "data": {
            "user_id": 1,
            "name": "aden",
            "email": "aden3@gmail.com",
            "account_number": "405811371",
            "previous_balance": 10000,
            "amount": 2000,
            "after_balance": 12000,
            "transaction_number": "PR7056CP1"
        }
    }
    '''

    def post(self, request: request) -> Response:
        form = DepositForm(data=request.data or None)
        if form.is_valid():
            user, transaction_log = form.save()
            data ={
                'messages': f'Proses deposit berhasil',
                'is_success': True
            }
            data['data'] = self.serialize_data(user, transaction_log)
            return Response(data=data, status=status.HTTP_200_OK)
        return ErrorResponse(form=form)

    def serialize_data(self, user: User, transaction_log: TransactionLog) -> dict:
        data = {
            "user_id": user.id,
            "name": user.name,
            "email": user.email,
            "account_number": user.account_number,
            "previous_balance": transaction_log.previous_balance,
            "amount": transaction_log.amount,
            "after_balance": transaction_log.after_balance,
            "transaction_number": transaction_log.transaction_number,
        }

        return data



class Withdraw(APIView):

    def post(self, request: request) -> Response:
        form = WithdrawForm(data=request.data or None)
        if form.is_valid():
            user, transaction_log = form.save()
            data ={
                'messages': f'Proses withdraw berhasil',
                'is_success': True
            }
            data['data'] = self.serialize_data(user, transaction_log)
            return Response(data=data, status=status.HTTP_200_OK)
        return ErrorResponse(form=form)

    def serialize_data(self, user: User, transaction_log: TransactionLog) -> dict:
        data = {
            "user_id": user.id,
            "name": user.name,
            "email": user.email,
            "account_number": user.account_number,
            "previous_balance": transaction_log.previous_balance,
            "amount": transaction_log.amount,
            "charge": transaction_log.charge,
            "after_balance": transaction_log.after_balance,
            "transaction_number": transaction_log.transaction_number,
        }

        return data