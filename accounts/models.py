from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_type = models.CharField(max_length=20, choices=[('parent', 'Parent'), ('child', 'Child')], default='parent')
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Parent')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

class Address(models.Model):
    person = models.OneToOneField('Person', on_delete=models.CASCADE, related_name='address_details')
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}, {}, {}, {}'.format(self.street, self.city, self.state, self.zip_code)
