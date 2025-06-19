from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):

    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )