from django import forms
from .models import CATEGORY_CHOICES
from django.core.validators import MinValueValidator

default_status = CATEGORY_CHOICES[0][0]


class ShopForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label='Заголовок')
    description = forms.CharField(max_length=2000, label='Описание')
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=True, label='Категория',
                               initial=default_status)
    amount = forms.IntegerField(validators=(MinValueValidator(0),), label='Остаток')
    price = forms.DecimalField(max_digits=7, decimal_places=2, label='Цена',)
