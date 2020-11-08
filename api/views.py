from rest_framework import viewsets
from .serializers import *

from accounts.models import Person


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
