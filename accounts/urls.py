from django.urls import path
from django.contrib.auth.decorators import login_required
from accounts import views

app_name='accounts'

urlpatterns = [
    path('', views.UserListView.as_view(), name='user_list'),
    path('create/', views.UserCreateView.as_view(), name='user_create'),
]
