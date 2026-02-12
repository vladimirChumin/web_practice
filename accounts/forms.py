from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()


class RegisterUser(forms.ModelForm):
    email = forms.EmailField(required=True, label="Электронная почта", widget=forms.EmailInput())

    name = forms.CharField(label="Имя пользователя", required=False)
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email")
        labels = {
            "username": "Логин",
            "email": "Электронная почта",
        }
        error_messages = {
            "email": {
                "invalid": "Некорректный email",
            }
        }

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Логин занят.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email занят.")
        return email

    def clean_password1(self):
        p1 = self.cleaned_data.get("password1")
        if p1:
            validate_password(p1)
        return p1

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")

        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Пароли не совпадают.")

        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.first_name = self.cleaned_data["name"]
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    pass
