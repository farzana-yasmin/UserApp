from django.test import TestCase
from django.urls import reverse
from accounts.models import Person, Address
from .serializers import PersonSerializer
from .views import PersonViewSet
from rest_framework.test import APIClient
from rest_framework import status

# Api TestCase
USER_URL = reverse('api:person-list')

class UserApiTest(TestCase):
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
        response = self.client.post(USER_URL, self.data, format="json")
        # import pdb
        # pdb.set_trace()
        self.assertEqual(response.data['first_name'], self.data['first_name'])
        self.assertEqual(response.data['city'], self.data['city'])
        self.assertEqual(response.status_code, 201)

    def test_user_list(self):
        response = self.client.get(USER_URL, format="json")
        self.assertEqual(response.status_code, 200)
        qs = Person.objects.filter(first_name="oma")
        self.assertEqual(qs.count(), 1)

    def test_user_details(self):
        qs = Person.objects.get(first_name="oma")
        response = self.client.get(USER_URL, args=[qs.id])
        import pdb
        pdb.set_trace()
        self.assertEqual(response.status_code, 200)

    def test_user_delete(self):
        response = self.client.delete('http://localhost:8000/api/user/3/')
        # import pdb
        # pdb.set_trace()
        self.assertEqual(response.status_code, 204)

    # def test_user_list(self):
    #     response = self.client.get(USER_URL)
    #     print(response.json())
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_user_details_retrive(self):
    #     response = self.client.get(reverse("api:person-detail", kwargs={"pk": 6}))
    #     print(response.json())
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data['first_name'], "Farzana")

    # def test_user_update(self):
    #     response = self.client.put(reverse("api:person-detail", kwargs={"pk": 6}), {"city": "Anchiano"})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(json.loads(response.content), {"id": 6, "first_name": "Farzana", "city": "Anchiano"})

    # def test_create_user_successful(self):
    #     data = {'first_name': 'oma',
    #             'last_name': 'gonza',
    #             'user_type': 'parent',
    #             'street': '2096 Starling Ave',
    #             'city': 'Bronx',
    #             'state': 'NY 10462',
    #             'zip_code': '43006'
    #             }
    #     res = self.client.post(USER_URL, data)
    #     # exists = Person.objects.filter(
    #     #             first_name = data['first_name'],
    #     #             ).exists()
                    
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(res.data, data)