from django.urls import path

from loratech_test.api.transactions.views import Deposit, Withdraw

app_name = 'transactions'

urlpatterns = [
    path('deposit', Deposit.as_view(), name="deposit"),
    path('withdraw', Withdraw.as_view(), name="withdraw")
]
