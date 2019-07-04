from django import forms


class UserForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=128)
    email = forms.EmailField()
    password = forms.CharField()
