from django import forms


class ChangePwForm(forms.Form):
    password0 = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()
