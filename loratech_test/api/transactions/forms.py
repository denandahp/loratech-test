from django import forms
from django.conf import settings
from django.db import transaction

from loratech_test.apps.transactions.model import Balance, TransactionLog
from loratech_test.apps.users.model import User
from loratech_test.core.utils import generate_code


class DepositForm(forms.Form):
    
    user_id = forms.IntegerField()
    amount = forms.IntegerField()
     
    def clean_user_id(self):
        user_id = self.cleaned_data['user_id']
        user = User.objects.filter(id=user_id).first()
        if not user:
            raise forms.ValidationError("User tidak ditemukan",
                                        code="user_not_exist")
        return user
    
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        minimal_deposit = settings.MINIMAL_DEPOSIT
        if amount < minimal_deposit:
            raise forms.ValidationError(f"Deposit kurang dari {minimal_deposit}",
                                        code="less_deposit")
        return amount
    
    def clean(self):
        data = super().clean()
        self.user = self.cleaned_data['user_id']
        self.balance = Balance.objects.get(user=self.user)
        return data
    
    def save(self):
        amount = self.cleaned_data['amount']
        previous_balance = self.balance.balance
        after_balance = previous_balance + amount

        with transaction.atomic():
            self.balance.balance = after_balance
            self.balance.save()

            transaction_log = TransactionLog(
                from_user=self.user,
                balance=self.balance,
                previous_balance=previous_balance,
                after_balance=after_balance,
                amount=amount,
                status=TransactionLog.STATUS.DEPOSIT,
                transaction_number=generate_code(settings.ACCOUNT_NUMBER_LENGTH)
            )
            transaction_log.save()

            return self.user, transaction_log


class WithdrawForm(forms.Form):
    
    user_id = forms.IntegerField()
    amount = forms.IntegerField()
     
    def clean_user_id(self):
        user_id = self.cleaned_data['user_id']
        user = User.objects.filter(id=user_id).first()
        if not user:
            raise forms.ValidationError("User tidak ditemukan",
                                        code="user_not_exist")
        return user
    
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        self.charger = 0
        minimal_withdraw = settings.MINIMAL_WITHDRAW
        if amount < minimal_withdraw:
            raise forms.ValidationError(f"Withdraw kurang dari {minimal_withdraw}",
                                        code="less_withdraw")

        # Calculate charger
        if amount in range(501, 5000, 1):
            self.charger = 10
        elif amount > 5001:
            self.charger = 20

        return amount
    
    def clean(self):
        data = super().clean()
        self.user = self.cleaned_data['user_id']
        self.balance = Balance.objects.get(user=self.user)
        if self.balance.balance <= settings.MINIMAL_WITHDRAW:
            error = forms.ValidationError(f'Saldo anda saat ini kurang dari {settings.MINIMAL_WITHDRAW}',
                                          code="less_balance")
            self.add_error('amount', error)

        return data
    
    def save(self):
        amount = self.cleaned_data['amount']
        previous_balance = self.balance.balance
        after_balance = previous_balance - amount - self.charger

        with transaction.atomic():
            self.balance.balance = after_balance
            self.balance.save()

            transaction_log = TransactionLog(
                from_user=self.user,
                balance=self.balance,
                previous_balance=previous_balance,
                after_balance=after_balance,
                amount=amount,
                charge=self.charger,
                status=TransactionLog.STATUS.WITHDRAW,
                transaction_number=generate_code(settings.ACCOUNT_NUMBER_LENGTH)
            )
            transaction_log.save()

            return self.user, transaction_log
