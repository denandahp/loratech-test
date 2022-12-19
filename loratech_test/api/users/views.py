from django.forms.models import model_to_dict

from loratech_test.api.response import ErrorResponse

from rest_framework import request, status
from rest_framework.response import Response
from rest_framework.views import APIView

from loratech_test.api.users.forms import UserForm
from loratech_test.apps.users.model import User
from loratech_test.core.utils import PaginatorPage

class DetailUsers(APIView):
    '''
    url= http://127.0.0.1:8000/api/users/detail?acc_number=1
    :param acc_number: account number user, delete param is true
    '''

    def get(self, request: request) -> Response:
        acc_number = request.GET.get('acc_number')
        if acc_number:
            user = User.objects.prefetch_related('balance_users').filter(account_number=acc_number).first()
            if not user:
                data ={
                    'messages': f'Nomor akun {acc_number} tidak ditemukan',
                    'is_success': False
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

            data ={
                'messages': f'Detail user {user}',
                'is_success': True,
                'data': self.serialize_data(user)
            }
            return Response(data=data, status=status.HTTP_200_OK)
    
    def serialize_data(self, user: User):
        balance = user.balance_users.first()
        data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "mobile_number": user.mobile_number,
            "is_active": user.is_active,
            "address": user.address,
            "account_number": user.account_number,
            "balance": balance.balance
        }

        return data


class IndexUsers(APIView):
    '''
    url= http://127.0.0.1:8000/api/users?page=1&limit=10
    :param page: Number of page
    :param limit: Number of page
    '''

    def get(self, request: request) -> Response:
        user_list = []
        limit = int(request.GET.get('limit', 1))
        users = User.objects.prefetch_related('balance_users')
        paginator = PaginatorPage(users, request.GET.get('page', 1), step=limit)
        for user in paginator.objects:
            user_list.append(DetailUsers.serialize_data(self, user))
        data = {
            'limit': limit,
            'paginator': {
                'next': paginator.next,
                'previous': paginator.previous
            },
            'data': user_list
        }
        return Response(data=data, status=status.HTTP_200_OK)


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