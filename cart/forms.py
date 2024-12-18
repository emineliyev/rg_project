from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control cart-quantity-input',
            'min': 1,
        }),
        initial=1
    )
    override_quantity = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

