from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(label="Логин", max_length=50)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
