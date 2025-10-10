from django import forms
from .models import Leader, Candidante
import re

class LoginForm(forms.Form):
    email = forms.CharField(label="Логин", max_length=50)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)


class RegisterLeaderForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Leader
        fields = ['name', 'email', "company", "city", 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 9:
            raise forms.ValidationError("Пароль должен быть не короче 9 символов")
        if not re.search(r"[A-Z]", password):
            raise forms.ValidationError("Пароль должен содержать хотя бы одну заглавную букву")
        if not re.search(r"\d", password):
            raise forms.ValidationError("Пароль должен содержать хотя бы одну цифру")
        if not re.search(r"[@$!%*?&.]", password):
            raise forms.ValidationError("Пароль должен содержать хотя бы один специальный символ")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("password2")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Пароли не совпадают")

class RegisterCandidanteForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Candidante
        fields = ['name', 'email', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 9:
            raise forms.ValidationError("Пароль должен быть не короче 9 символов")
        if not re.search(r"[A-Z]", password):
            raise forms.ValidationError("Пароль должен содержать хотя бы одну заглавную букву")
        if not re.search(r"\d", password):
            raise forms.ValidationError("Пароль должен содержать хотя бы одну цифру")
        if not re.search(r"[@$!%*?&.]", password):
            raise forms.ValidationError("Пароль должен содержать хотя бы один специальный символ")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("password2")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Пароли не совпадают")

class BanUserForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea, label="Причина бана")
    days = forms.IntegerField(label="Срок бана (дней)", min_value=1)