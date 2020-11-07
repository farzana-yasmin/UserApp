from django.shortcuts import render
from django.views.generic import TemplateView

class UserListView(TemplateView):
    template_name = 'accounts/list.html'
