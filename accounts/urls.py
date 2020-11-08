from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('', views.UserListView.as_view(), name='user_list'),
    path('create/', views.UserCreateView.as_view(), name='user_create'),
    path('edit/<pk>/', views.UserChangeView.as_view(), name='user_edit'),
    path('delete/<pk>/', views.UserDeleteView.as_view(), name='user_delete'),
]
