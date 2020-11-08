from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import *


class PersonSerializer(serializers.ModelSerializer):
    """
    Author: Farzana Yasmin.

    Purpose: Serializer for get, post, put, delete user.
    Pre condition: N/A.
    Post condition: N/A.
    Library dependency: N/A.
    Database Interaction: accounts.models.Person will be hit to fetch all the users.
    File Location: api/serializers.py.
    Testing Information: Success.

    Args:
        serializers.ModelSerializer: rest_framework

    Returns:
        Object list
    """

    street = serializers.CharField(max_length=100, required=False)
    city = serializers.CharField(max_length=100, required=False)
    state = serializers.CharField(max_length=100, required=False)
    zip_code = serializers.CharField(max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if kwargs.get('instance'):
            self.fields['parent_id'].queryset = Person.objects.exclude(id=kwargs.get('instance').id)

    def validate(self, data):
        """
        Purpose: Validation for request data.

        Args:
            data: request data

        Returns:
            data
        """

        msg = "This field is required"

        if data['user_type'] == 'child':
            if not 'parent_id' in data or data['parent_id'] is None:
                raise ValidationError({'parent_id': [msg]})
        else:
            if not 'street' in data:
                raise ValidationError({'street': [msg]})
            if not 'city' in data:
                raise ValidationError({'city': [msg]})
            if not 'state' in data:
                raise ValidationError({'state': [msg]})
            if not 'zip_code' in data:
                raise ValidationError({'zip_code': [msg]})
        return data

    class Meta:
        model = Person
        fields = ['id', 'first_name', 'last_name', 'user_type', 'parent_id', 'street', 'city', 'state', 'zip_code']

    def to_representation(self, instance):
        """
        Purpose: Represent all users.

        Args:
            instance: object instance

        Returns:
            object list
        """

        rep = super().to_representation(instance)

        try:
            rep['street'] = instance.address_details.street
            rep['city'] = instance.address_details.city
            rep['state'] = instance.address_details.state
            rep['zip_code'] = instance.address_details.zip_code
        except:
            pass

        return rep

    def create(self, validated_data):
        """
        Author: Farzana Yasmin.

        Purpose: Submit data.
        Pre condition: N/A.
        Post condition: N/A.
        Library dependency: N/A.
        Database Interaction: accounts.models.Person will be hit to create an users and
                          also hit accounts.models.Address for creating address details.
        File Location: api/serializers.py.
        Testing Information: Success.

        Args:
            validated_data

        Returns:
            Person object
        """

        person = Person.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            user_type=validated_data['user_type'],
            parent_id=validated_data['parent_id'] if validated_data['user_type'] == 'child' else None,
        )

        if validated_data['user_type'] == 'parent':
            Address.objects.create(
                person=person,
                street=validated_data['street'],
                city=validated_data['city'],
                state=validated_data['state'],
                zip_code=validated_data['zip_code'],
            )

        return person

    def update(self, instance, validated_data):
        """
        Author: Farzana Yasmin.

        Purpose: Update specific user.
        Pre condition: N/A.
        Post condition: N/A.
        Library dependency: N/A.
        Database Interaction: accounts.models.Person will be hit to update the specific user and
                          also hit accounts.models.Address for creating/updating address details.
        File Location: api/serializers.py.
        Testing Information: Success.

        Args:
            validated_data, instance

        Returns:
            Person object
        """

        Person.objects.filter(id=instance.id). \
            update(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            user_type=validated_data['user_type'],
            parent_id=validated_data['parent_id'] if validated_data['user_type'] == 'child' else None,
        )

        if validated_data['user_type'] == 'parent':
            Address.objects.update_or_create(
                person=instance,
                defaults={
                    'street': validated_data.get('street'),
                    'city': validated_data.get('city'),
                    'state': validated_data.get('state'),
                    'zip_code': validated_data.get('zip_code')
                }
            )
        else:
            Address.objects.filter(person=instance).delete()

        return Person.objects.get(id=instance.id)
