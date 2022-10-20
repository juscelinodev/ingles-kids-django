from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    # username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields['email'].widget.attrs.update({'placeholder': 'Insira o e-mail'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Insira uma senha'})

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)

            if self.user is None:
                raise forms.ValidationError("Usuário não existe.")
            if not self.user.check_password(password):
                raise forms.ValidationError("Senha incorreta.")
            if not self.user.is_active:
                raise forms.ValidationError("Usuário não está ativo.")

        return super(UserLoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user


class UserRegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].icon = '<span class="input-field-icon"><i class="fas fa-envelope"></i></span>'
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Insira o nome'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Insira o sobrenome'})
        self.fields['username'].widget.attrs.update({'placeholder': 'Usuário'})
        self.fields['email'].widget.attrs.update({'placeholder': 'E-mail'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Insira a senha'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Insira novamente a senha'})
        # self.fields['email'].widget.attrs['placeholder'] = self.fields['email'].label or 'email@address.nl'

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2")

        # widgets = {
        #     'password1': forms.TextInput(attrs={'placeholder': 'Password'}),
        #     'password2': forms.TextInput(attrs={'placeholder': 'Repeat your password'}),
        # }

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise forms.ValidationError('Insira um e-mail válido.')
        return email

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update({'placeholder': 'Insira o nome'})
        self.fields["last_name"].widget.attrs.update({'placeholder': 'Insira o sobrenome'})

    class Meta:
        model = User
        fields = ["first_name", "last_name"]
