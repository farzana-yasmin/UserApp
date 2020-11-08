from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Person, Address
from .forms import UserCreateForm


class UserListView(ListView):
    template_name = 'accounts/list.html'
    model = Person


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = 'accounts/create.html'
    form_class = UserCreateForm
    success_url = '/'
    success_message = "%(first_name)s %(last_name)s successfully saved."

    def form_valid(self, form):
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
    template_name = 'accounts/update.html'
    model = Person
    form_class = UserCreateForm
    success_url = '/'
    success_message = "%(first_name)s %(last_name)s successfully updated."

    def form_valid(self, form):
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
    model = Person
    success_message = "%(first_name)s %(last_name)s is deleted."
    template_name = 'accounts/user_confirm_delete.html'
    success_url = reverse_lazy('accounts:user_list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(UserDeleteView, self).delete(request, *args, **kwargs)
