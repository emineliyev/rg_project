from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'fin_code', 'email',
            'country', 'city', 'address', 'postal_code', 'phone_number'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'last_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'fin_code': forms.TextInput(attrs={'readonly': 'readonly'}),
            'email': forms.EmailInput(attrs={'readonly': 'readonly'}),
            'country': forms.TextInput(attrs={'readonly': 'readonly'}),
            'city': forms.TextInput(attrs={'readonly': 'readonly'}),
            'address': forms.TextInput(attrs={'readonly': 'readonly'}),
            'postal_code': forms.TextInput(attrs={'readonly': 'readonly'}),
            'phone_number': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Получаем пользователя, если передан
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            # Предзаполняем данные из модели пользователя
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['fin_code'].initial = user.fin_code
            self.fields['email'].initial = user.email
            self.fields['phone_number'].initial = user.phone_number
            self.fields['address'].initial = user.address
            self.fields['postal_code'].initial = user.postal_code
            if user.country:
                self.fields['country'].initial = user.country.name
            if user.city:
                self.fields['city'].initial = user.city.name
