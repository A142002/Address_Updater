from django.urls import path
from .views import CustomLoginView, AddressList, AddressDeleteSelected, RegisterPage, AddressDelete, AddressUpdate, AddressDetail, AddressCreate, AddressConfirmDeleteView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('', AddressList.as_view(), name='address'),  # Changed name to 'address-list' to differentiate from detail view
    path('address/<int:pk>/', AddressDetail.as_view(), name='address-detail'),  # Changed URL pattern to 'address/<int:pk>/' as referenced in your template
    path('address-create/', AddressCreate.as_view(), name='address-create'),  # Changed URL pattern to 'address-create/' for consistency
    path('address-edit/<int:pk>/', AddressUpdate.as_view(), name='address-edit'),  # Added URL pattern for editing an address
    path('address-delete/<int:pk>/', AddressDelete.as_view(), name='address-delete'),
    path('address-delete-selected/', AddressDeleteSelected.as_view(), name='address-delete-selected'),
    path('address-delete-confirm/<int:pk>/', AddressConfirmDeleteView.as_view(), name='address-delete-confirm'),
]
