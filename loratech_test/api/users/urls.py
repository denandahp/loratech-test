from django.urls import path

from loratech_test.api.users.views import CreateUsers, IndexUsers

app_name = 'users'

urlpatterns = [
    path('', IndexUsers.as_view(), name="index_user"),
    path('add', CreateUsers.as_view(), name="create_user")
]
