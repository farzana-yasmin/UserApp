from django import forms
from .models import Person, Address

class UserCreateForm(forms.ModelForm):
    street = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    zip_code = forms.CharField(max_length=100)


    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'user_type', 'parent_id')