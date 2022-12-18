from django import forms
from django.conf import settings
from django.db import transaction

from loratech_test.apps.transactions.model import Balance, TransactionLog
from loratech_test.apps.users.model import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'password', 'tax_number', 'email', 'mobile_number', 'address']
    
    deposit = forms.IntegerField()
     
    def clean_email(self):
        email = self.cleaned_data['email']
        is_exist = User.objects.filter(email=email).exists()
        if is_exist:
            raise forms.ValidationError("Email sudah ada yang menggunakan",
                                        code="email_already_exist")
        return email.lower()
    
    def clean_mobile_number(self):
        mobile_number = self.cleaned_data['mobile_number']
        is_exist = User.objects.filter(mobile_number=mobile_number).exists()
        if is_exist:
            raise forms.ValidationError("Nomor sudah ada yang menggunakan",
                                        code="mobile_number_already_exist")
        return mobile_number
    
    def clean_deposit(self):
        deposit = self.cleaned_data['deposit']
        intial_deposit = settings.INITIAL_DEPOSIT
        if deposit <= intial_deposit:
            raise forms.ValidationError(f"Saldo awal kurang dari {intial_deposit}",
                                        code="less_balance")
        return deposit

    def clean_tax_number(self):
        tax_number = self.cleaned_data['tax_number']
        if len(tax_number) < settings.TAX_ID_LENGTH:
            raise forms.ValidationError(f"Panjang Tax ID lebih dari {settings.TAX_ID_LENGTH}",
                                        code="less_balance")
        is_exist = User.objects.filter(tax_number=tax_number).exists()
        if is_exist:
            raise forms.ValidationError(f"Tax ID sudah terdaftar",
                                        code="tax_number_already_exist")
        return tax_number
    
    def save(self, *args, **kwargs):
        with transaction.atomic():
            user = super().save(*args, **kwargs)
            user.set_password(self.cleaned_data['password'])
            user.save()

            balance = Balance(
                user=user,
                balance=self.cleaned_data['deposit']
            )
            balance.save()

            transaction_log = TransactionLog(
                from_user=user,
                balance=balance,
                previous_balance=0,
                after_balance=self.cleaned_data['deposit'],
                amount=self.cleaned_data['deposit'],
                status=TransactionLog.STATUS.DEPOSIT
            )
            transaction_log.save()
            return user, balance, transaction_log
