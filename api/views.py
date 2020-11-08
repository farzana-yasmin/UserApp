from rest_framework import viewsets
from .serializers import *

from accounts.models import Person


class PersonViewSet(viewsets.ModelViewSet):
    """
    Author: Farzana Yasmin.

    Purpose: Provides create(), update(), retrieve(), destroy(), list() actions.
    Pre condition: N/A.
    Post condition: N/A.
    Library dependency: N/A.
    Database Interaction: accounts.models.Person will be hit to fetch all the users.
    File Location: api/views.py.
    Testing Information: Success.

    Args:
        viewsets.ModelViewSet: rest_framework

    Returns:
        All object list
    """

    queryset = Person.objects.all()
    serializer_class = PersonSerializer
