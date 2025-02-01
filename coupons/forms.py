from django import forms


class CouponApplyForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'id': 'coupon-field', 'placeholder': 'Kupon kodunu daxil edin'}), label='')
