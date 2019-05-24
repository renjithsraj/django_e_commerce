from buyer.models import Buyer
from django import forms
from django.core.exceptions import ValidationError
import re


class BuyerCreationForm(forms.Form):
    name = forms.CharField(
        label='Enter Username', min_length=4, max_length=150)
    username = forms.CharField(
        label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(
        label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Enter Confirm password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        pattern = r"\"?([-a-zA-Z0-9.`?{}]\w+)\"?"
        pattern_1 = re.compile(pattern)
        if not re.match(pattern_1, username):
            raise ValidationError("Please enter valid username")
        r = Buyer.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = Buyer.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        return password2

    def save(self, commit=True):
        fullname = self.cleaned_data['name']
        firstname = fullname.strip().split(' ')[0]
        lastname = ' '.join((fullname + ' ').split(' ')[1:]).strip()

        user = Buyer.objects.create_user(
            first_name = firstname,
            last_name = lastname,
            username = self.cleaned_data['username'],
            email = self.cleaned_data['email'],
            password = self.cleaned_data['password1'],
            is_active = False
        )
        return user
