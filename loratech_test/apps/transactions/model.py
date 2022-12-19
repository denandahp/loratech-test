from django.conf import settings
from django.db import models

from loratech_test.apps.users.model import User
from loratech_test.core.utils import generate_code

from model_utils import Choices

class Balance(models.Model):
    user = models.ForeignKey(User, related_name='balance_users', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    balance = models.IntegerField(default=0, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user} - {self.balance}"


class TransactionLog(models.Model):
    from_user = models.ForeignKey(User, related_name='from_users', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, 
                                related_name='to_users',
                                on_delete=models.CASCADE,
                                blank=True, null=True)
    balance = models.ForeignKey(Balance, related_name='balances', on_delete=models.CASCADE)
    after_balance = models.IntegerField(default=0, blank=True, null=True)
    previous_balance = models.IntegerField(default=0, blank=True, null=True)
    amount = models.IntegerField(default=0, blank=True, null=True)
    charge = models.IntegerField(default=0, blank=True, null=True)
    transaction_number = models.CharField(max_length=10, db_index=True, default=generate_code(settings.ACCOUNT_NUMBER_LENGTH))

    STATUS = Choices(
        (1, "WITHDRAW", "Withdraw"),
        (2, "DEPOSIT", "Deposit"),
        (3, "TRANSFER", "Transfer"),
    )
    status = models.PositiveIntegerField(choices=STATUS)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.transaction_number} - {self.from_user} - {self.status}"
