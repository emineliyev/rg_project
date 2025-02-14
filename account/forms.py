from django import forms
from account.models import Account


class UserRegisterForm(forms.ModelForm):
    fin_code = forms.CharField(widget=forms.TextInput())  # ✅ Добавили fin_code в форму
    email = forms.EmailField(widget=forms.EmailInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Account
        fields = ['fin_code', 'email', 'password1', 'password2']  # ✅ fin_code теперь обязателен

    def clean_fin_code(self):
        fin_code = self.cleaned_data.get("fin_code")
        if not fin_code:
            raise forms.ValidationError("Fin kod обязательно!")
        if Account.objects.filter(fin_code=fin_code).exists():
            raise forms.ValidationError("Этот Fin kod уже зарегистрирован.")
        return fin_code

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Şifrələr üst-üstə düşmür.")

        return cleaned_data

    def save(self, commit=True):
        email = self.cleaned_data['email']
        fin_code = self.cleaned_data['fin_code']  # ✅ Теперь `fin_code` берется из формы
        password = self.cleaned_data['password1']

        user = Account.objects.create_user(
            email=email,
            fin_code=fin_code,  # ✅ fin_code передается в модель
            password=password
        )

        if commit:
            user.save()

        return user


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


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
