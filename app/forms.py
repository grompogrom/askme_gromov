from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from app.models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=4, widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_check']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        validate_email(email)
        exists = User.objects.filter(email=email).all().count()
        if exists:
            raise ValidationError('Email already registered')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        exists = User.objects.filter(username=username).all().count()
        if exists:
            raise ValidationError('Username already used')
        return username

    def clean(self):
        password = self.cleaned_data.get('password')
        password_check = self.cleaned_data.get('password_check')

        if password != password_check:
            raise ValidationError('Passwords do not match')

    def save(self, **kwargs):
        self.cleaned_data.pop('password_check')
        print(self.cleaned_data)
        user = User.objects.create_user(**self.cleaned_data)
        Profile.objects.create(user=user)
        return user
