from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView
from .models import Person, Address
from .forms import UserCreateForm
from django.http import HttpResponseRedirect

class UserListView(ListView):
    template_name = 'accounts/list.html'
    model = Person

class UserCreateView(CreateView):
    template_name = 'accounts/create.html'
    form_class  = UserCreateForm
    success_url = '/'

    # def get_context_data(self, **kwargs):
    #     context = super(UserCreateView, self).get_context_data(**kwargs)
    #     if 'form' not in context:
    #         context['form'] = self.form_class(request=self.request)
    #     if 'form2' not in context:
    #         context['form2'] = self.second_form_class(request=self.request)
    #     return context

    # def get_object(self):
    #     return get_object_or_404(Person, pk=self.request.session['value_here'])

    def form_invalid(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        address_obj=Address(
            person=self.object, 
            street = self.request.POST.get('street'),
            city = self.request.POST.get('city'),
            state = self.request.POST.get('state'),
            zip_code = self.request.POST.get('zip_code'),
            )
        address_obj.save()

        return HttpResponseRedirect(self.success_url)