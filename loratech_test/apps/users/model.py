
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from loratech_test.core.utils import generate_code_number


class User(AbstractBaseUser):
    name = models.CharField(max_length=25)
    email = models.EmailField('email address', unique=True, max_length=255, blank=True, null=True)
    mobile_number = models.CharField(verbose_name='Mobile Number', max_length=30, unique=True,
                                     blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)
    address = models.TextField(blank=True, default='')
    tax_number = models.CharField(max_length=7, db_index=True, default=generate_code_number(settings.TAX_ID_LENGTH))
    account_number = models.CharField(max_length=10, db_index=True, default=generate_code_number(settings.ACCOUNT_NUMBER_LENGTH))
    created = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'

    def __str__(self) -> str:
        return self.name
