from django.contrib import admin

from loratech_test.apps.transactions.model import TransactionLog, Balance

admin.site.register(TransactionLog)
admin.site.register(Balance)
