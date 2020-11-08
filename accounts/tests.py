from django.test import TestCase
from .forms import UserCreateForm


class UserFormTest(TestCase):
    def test_user_form(self):
        form_data = {'first_name': 'oma',
                     'last_name': 'gonza',
                     'user_type': 'parent',
                     'street': '2096 Starling Ave',
                     'city': 'Bronx',
                     'state': 'NY 10462',
                     'zip_code': '43006'
                     }
        form = UserCreateForm(data=form_data)
        self.assertTrue(form.is_valid())
