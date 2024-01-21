from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm, PasswordResetForm
from django import forms
from catalog.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean_email(self):
        """
        Проверка email на уникальность
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Такой email уже используется в системе')
        return email


class UserForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'country', 'phone', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        phone_number = self.fields['phone'].widget

        self.fields['password'].widget = forms.HiddenInput()
        phone_number.attrs['class'] = "form-control bfh-phone"
        phone_number.attrs['data-format'] = "+7 (ddd) ddd-dd-dd"
        phone_number.attrs['value'] = "9999999999"


class PasswordRecoveryForm(forms.Form):
    email = forms.EmailField(label='Email')