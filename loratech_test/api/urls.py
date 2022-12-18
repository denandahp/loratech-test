from django.urls import include, path


app_name = 'api'

urlpatterns = [
    path('users/', include(
        'loratech_test.api.users.urls', namespace='users')),
    path('transactions/', include(
        'loratech_test.api.transactions.urls', namespace='transactions')),
]
