from django import forms

class CartAddForm(forms.Form):
    quantity = forms.IntegerField(max_value=9, min_value=1)

class CouponForm(forms.Form):
    coupon_code = forms.CharField()