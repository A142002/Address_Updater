from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponseRedirect
from .models import Address
from django.forms import Form
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('address')

class RegisterPage(CreateView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('address')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('address')
        return super().get(*args, **kwargs)

class AddressList(LoginRequiredMixin, ListView):
    model = Address
    context_object_name = "locations"
    paginate_by = 4  # Pagination

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        search_input = self.request.GET.get('search-area')
        if search_input:
            queryset = queryset.filter(street_address__icontains=search_input)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = self.get_queryset().filter(country=False).count()
        context['search_input'] = self.request.GET.get('search-area', '')
        return context

class AddressDetail(LoginRequiredMixin, DetailView):
    model = Address
    context_object_name = "location"
    template_name = 'base/address.html'

class AddressCreate(LoginRequiredMixin, CreateView):
    model = Address
    fields = ['street_address', 'city', 'state', 'country', 'zip_code']
    success_url = reverse_lazy('address')  # Ensure consistent URL naming

    def form_valid(self, form):
        instance = form.save(commit=False)
        existing_address = Address.objects.filter(
            street_address=instance.street_address,
            city=instance.city,
            state=instance.state,
            country=instance.country,
            zip_code=instance.zip_code
        ).first()

        if existing_address:
            form.add_error(None, 'Entered address already exists.')
            self.address_already_exists = True
            return self.form_invalid(form)
        else:
            instance.user = self.request.user
            instance.save()
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['address_already_exists'] = getattr(self, 'address_already_exists', False)
        return context

class AddressUpdate(LoginRequiredMixin, UpdateView):
    model = Address
    fields = ['street_address', 'city', 'state', 'country', 'zip_code']
    success_url = reverse_lazy('address')

    def form_valid(self, form):
        instance = form.save(commit=False)
        existing_address = Address.objects.filter(
            street_address=instance.street_address,
            city=instance.city,
            state=instance.state,
            country=instance.country,
            zip_code=instance.zip_code
        ).exclude(pk=instance.pk).first()

        if existing_address:
            form.add_error(None, 'Entered address already exists.')
            self.address_already_exists = True
            return self.form_invalid(form)
        else:
            instance.user = self.request.user
            instance.save()
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['address_already_exists'] = getattr(self, 'address_already_exists', False)
        return context

class AddressDelete(LoginRequiredMixin, DeleteView):
    model = Address
    context_object_name = 'location'
    success_url = reverse_lazy('address')  # Ensure consistent URL naming

class AddressDeleteSelected(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        selected_addresses = request.POST.getlist('selected_addresses')
        Address.objects.filter(pk__in=selected_addresses).delete()
        return HttpResponseRedirect(reverse_lazy('address'))
    
class AddressConfirmDeleteView(DeleteView):
    model = Address
    template_name = 'base/address_confirm_delete.html'
    success_url = reverse_lazy('address')
