from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=100, validators=[RegexValidator(r'^[a-zA-Z\s]*$', 'City must contain only letters and spaces.')])
    state = models.CharField(max_length=100, validators=[RegexValidator(r'^[a-zA-Z\s]*$', 'State must contain only letters and spaces.')])
    country = models.CharField(max_length=100, validators=[RegexValidator(r'^[a-zA-Z\s]*$', 'Country must contain only letters and spaces.')])
    zip_code = models.CharField(max_length=6, validators=[RegexValidator(r'^\d{6}$', "ZIP code must contain exactly 6 digits.")])

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.street_address

    class Meta:
        ordering = ['country']
