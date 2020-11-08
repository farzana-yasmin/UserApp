from django.test import TestCase
from django.urls import reverse

from accounts.models import Person, Address
from rest_framework.test import APIClient
from rest_framework import status

# Api TestCase
USER_URL = reverse('api:person-list')


class UserApiTest(TestCase):
    """ Unit test for user api. """

    def setUp(self):
        self.client = APIClient()
        self.data = {'first_name': 'oma',
                     'last_name': 'gonza',
                     'user_type': 'parent',
                     'parent_id': None,
                     'street': '2096 Starling Ave',
                     'city': 'Bronx',
                     'state': 'NY 10462',
                     'zip_code': '43006'
                     }
        person = Person.objects.create(
            first_name=self.data['first_name'],
            last_name=self.data['last_name'],
            user_type=self.data['user_type'],
            parent_id=self.data['parent_id'],
        )

        if self.data['user_type'] == 'parent':
            Address.objects.create(
                person=person,
                street=self.data['street'],
                city=self.data['city'],
                state=self.data['state'],
                zip_code=self.data['zip_code'],
            )

    def test_user_create(self):
        """ Unit test for creating user. """

        response = self.client.post(USER_URL, self.data, format="json")
        self.assertEqual(response.data['first_name'], self.data['first_name'])
        self.assertEqual(response.data['city'], self.data['city'])
        self.assertEqual(response.status_code, 201)
        print("Successfully created an object")

    def test_user_list(self):
        """ Unit test for listing user. """

        response = self.client.get(USER_URL, format="json")
        self.assertEqual(response.status_code, 200)
        qs = Person.objects.filter(first_name="oma")
        self.assertEqual(qs.count(), 1)
        print("List of object")

    def test_user_details(self):
        """ Unit test for updating the specific user. """

        person_objs = Person.objects.all()
        if person_objs:
            data = {
                    'id': person_objs[0].id,
                    'first_name': "Farzana",
                    'last_name': 'Yasmin',
                    'user_type': person_objs[0].user_type,
                    'street': person_objs[0].address_details.street,
                    'city': person_objs[0].address_details.city,
                    'state': person_objs[0].address_details.state,
                    'zip_code': person_objs[0].address_details.zip_code,
                    }
            response = self.client.patch(reverse("api:person-detail", args=[person_objs[0].id]), data, format='json')
            # import pdb
            # pdb.set_trace()
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            print("Updated an object")

    def test_user_delete(self):
        """ Unit test for deleting the specific user. """

        person_objs = Person.objects.all()
        if person_objs:
            response = self.client.delete(reverse('api:person-detail', args=[person_objs[0].id]))
            self.assertEqual(response.status_code, 204)
            print("Successfully deleted an object")
