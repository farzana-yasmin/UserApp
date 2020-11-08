from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Person, Address
from .forms import UserCreateForm


class UserListView(ListView):
    """
    Author: Farzana Yasmin.
    Purpose: List of all users.
    Pre condition: N/A.
    Post condition: N/A.
    Library dependency: N/A.
    Database Interaction: accounts.models.Person will be hit to fetch all the users.
    File Location: accounts/views.py.

    Args:
        ListView: django.views.generic

    Returns:
        Object list
    """

    template_name = 'accounts/list.html'
    model = Person


class UserCreateView(SuccessMessageMixin, CreateView):
    """
    Author: Farzana Yasmin.
    Purpose: Create an user.
    Pre condition: N/A.
    Post condition: N/A.
    Library dependency: N/A.
    Database Interaction: accounts.models.Person will be hit to create an users and
                          also hit accounts.models.Address for creating address details.
    File Location: accounts/views.py.
    Testing Information: Success.

    Args:
        SuccessMessageMixin: django.contrib.messages.views
        CreateView: django.views.generic

    Returns:
        None
    """

    template_name = 'accounts/create.html'
    form_class = UserCreateForm
    success_url = '/'
    success_message = "%(first_name)s %(last_name)s successfully saved."

    def form_valid(self, form):
        """
        Author: Farzana Yasmin.

        Purpose: Submit the user create request & save to the database.
        Pre condition: N/A.
        Post condition: N/A.
        Library dependency: N/A.
        Database Interaction: accounts.models.Person will be hit to create an users and
                          also hit accounts.models.Address for creating address details.
        File Location: accounts/views.py.
        Testing Information: Success.
        Args:
            form: UserCreateForm

        Returns:
            django.http.HttpResponseRedirect|django.http.HttpResponseRedirectPermanent
        """

        self.object = form.save(commit=False)
        self.object.save()

        if self.object.user_type == 'parent':
            address_obj = Address(
                person=self.object,
                street=self.request.POST.get('street'),
                city=self.request.POST.get('city'),
                state=self.request.POST.get('state'),
                zip_code=self.request.POST.get('zip_code'),
            )
            address_obj.save()

        return super().form_valid(form)


class UserChangeView(SuccessMessageMixin, UpdateView):
    """
    Author: Farzana Yasmin.
    Purpose: Update the specific user.
    Pre condition: N/A.
    Post condition: N/A.
    Library dependency: N/A.
    Database Interaction: accounts.models.Person will be hit to update the specified users and
                          also hit accounts.models.Address for creating/updating address details.
    File Location: accounts/views.py.

    Args:
        SuccessMessageMixin: django.contrib.messages.views
        UpdateView: django.views.generic

    Returns:
        None
    """

    template_name = 'accounts/update.html'
    model = Person
    form_class = UserCreateForm
    success_url = '/'
    success_message = "%(first_name)s %(last_name)s successfully updated."

    def form_valid(self, form):
        """
        Author: Farzana Yasmin.
        Purpose: Submit the user update request & save to the database.
        Pre condition: N/A.
        Post condition: N/A.
        Library dependency: N/A.
        Database Interaction: accounts.models.Person model will be hit to update the specific user and
                              accounts.models.Address model also hit to create/update address details.
        File Location: accounts/views.py.
        Args:
            form: UserCreateForm

        Returns:
            django.http.HttpResponseRedirect|django.http.HttpResponseRedirectPermanent
        """

        self.object = form.save(commit=False)
        self.object.save()

        if self.object.user_type == 'parent':
            Address.objects.update_or_create(
                person=self.object,
                defaults={
                    'street': self.request.POST.get('street'),
                    'city': self.request.POST.get('city'),
                    'state': self.request.POST.get('state'),
                    'zip_code': self.request.POST.get('zip_code')
                }
            )
        else:
            Address.objects.filter(person=self.object).delete()

        return super().form_valid(form)


class UserDeleteView(SuccessMessageMixin, DeleteView):
    """
    Author: Farzana Yasmin.

    Purpose: Delete the specified user.
    Pre condition: N/A.
    Post condition: N/A.
    Library dependency: N/A.
    Database Interaction: accounts.models.Person will be hit to delete the specified user.
    File Location: accounts/views.py.

    Args:
        SuccessMessageMixin: django.contrib.messages.views
        DeleteView: django.views.generic.DeleteView

    Returns:
        None
    """
    model = Person
    success_message = "%(first_name)s %(last_name)s is deleted."
    template_name = 'accounts/user_confirm_delete.html'
    success_url = reverse_lazy('accounts:user_list')

    def delete(self, request, *args, **kwargs):
        """
         Author: Farzana Yasmin.

         Purpose: To delete the specified user.
         Pre condition: N/A.
         Post condition: N/A.
         Library dependency: N/A.
         Database Interaction: accounts.models.Person model will be hit to delete the specified user.
         File Location: accounts/views.py.

         Args:
             request: django.http.HttpRequest.
             *args: Internal arguments that will be handled by django.
             **kwargs: Internal key word arguments that will be handled by django.

         Returns:
             django.http.HttpResponseRedirect|django.http.HttpResponseRedirectPermanent
         """

        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(UserDeleteView, self).delete(request, *args, **kwargs)
