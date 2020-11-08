from django import forms
from .models import Person


class UserCreateForm(forms.ModelForm):
    street = forms.CharField(max_length=100, required=False)
    city = forms.CharField(max_length=100, required=False)
    state = forms.CharField(max_length=100, required=False)
    zip_code = forms.CharField(max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs['instance']:
            self.fields['parent_id'].queryset = Person.objects.exclude(id=kwargs['instance'].id)

            try:
                self.fields['street'].initial = kwargs['instance'].address_details.street
                self.fields['city'].initial = kwargs['instance'].address_details.city
                self.fields['state'].initial = kwargs['instance'].address_details.state
                self.fields['zip_code'].initial = kwargs['instance'].address_details.zip_code
            except:
                pass

    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'user_type', 'parent_id')

    def clean(self):
        cleaned_data = self.cleaned_data
        user_type = cleaned_data.get("user_type")

        msg = "This field is required"

        if user_type == 'parent':
            if cleaned_data.get("street") in [None, '']:
                self._errors['street'] = self.error_class([msg])

            if cleaned_data.get("city") in [None, '']:
                self._errors['city'] = self.error_class([msg])

            if cleaned_data.get("state") in [None, '']:
                self._errors['state'] = self.error_class([msg])

            if cleaned_data.get("zip_code") in [None, '']:
                self._errors['zip_code'] = self.error_class([msg])
        else:
            if cleaned_data.get("parent_id") in [None, '']:
                self._errors['parent_id'] = self.error_class([msg])

        return cleaned_data
