from django import forms
from django.contrib.auth.forms import User
from account.models import Account


class UserRegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput())
    name = forms.CharField(widget=forms.TextInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Account  # Замените на вашу модель пользователя
        fields = ['name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError("Bu e-poçtu olan istifadəçi artıq mövcuddur.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Şifrələr üst-üstə düşmür.")

        return cleaned_data

    def save(self, commit=True):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']

        # Create a new user using your custom manager
        user = Account.objects.create_user(
            email=email,
            password=password
        )

        if commit:
            user.save()

        return user


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())




# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Account
#         fields = ['email', 'first_name', 'last_name', 'fin_code', 'phone_number', 'country', 'city', 'address',
#                   'postal_code']
#         widgets = {
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'first_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'last_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'fin_code': forms.TextInput(attrs={'class': 'form-control'}),
#             'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
#             'country': forms.Select(attrs={'class': 'form-control'}),
#             'city': forms.Select(attrs={'class': 'form-control'}),
#             'address': forms.TextInput(attrs={'class': 'form-control'}),
#             'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
#         }


class ProfileForm(forms.ModelForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False,
        label="Старый пароль"
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False,
        label="Новый пароль"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False,
        label="Подтверждение нового пароля"
    )

    class Meta:
        model = Account
        fields = ['email', 'first_name', 'last_name', 'fin_code', 'phone_number', 'country', 'city', 'address',
                  'postal_code']
        widgets = {
            'email': forms.EmailInput(),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'fin_code': forms.TextInput(),
            'phone_number': forms.TextInput(),
            'country': forms.Select(),
            'city': forms.Select(),
            'address': forms.TextInput(),
            'postal_code': forms.TextInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password or confirm_password:
            if not old_password:
                raise forms.ValidationError("Для изменения пароля укажите старый пароль.")
            if new_password != confirm_password:
                raise forms.ValidationError("Новый пароль и его подтверждение не совпадают.")
        return cleaned_data
