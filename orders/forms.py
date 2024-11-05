import datetime
from django import forms
from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from orders.models import Order


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_active':
                field.widget.attrs['class'] = 'form-control'


class OrderForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Order
        fields = ('phone', 'address', 'delivery_date')
        widgets = {
            "delivery_date": DateTimePickerInput(
                options={
                    "format": "DD-MM-YYYY HH:mm",
                    "showTodayButton": False,
                    "minDate": (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
                },
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control bfh-phone",
                    "data-format": "+7 (ddd) ddd-dd-dd",
                },
            ),
        }
