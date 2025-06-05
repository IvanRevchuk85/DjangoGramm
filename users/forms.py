from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        error_messages={
            'required': 'Пожалуйста, введите ваш email.',
            'invalid': 'Введите корректный email-адрес.'
        }
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Пользователь с таким email уже существует.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return password2


class EditProfileForm(forms.ModelForm):
    """User profile editing form"""
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'bio', 'avatar']

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar and avatar.size > 2 * 1024 * 1024:  # 2MB limit
            raise forms.ValidationError(
                "Размер изображения не должен превышать 2МБ")
        return avatar
