from django import forms

from catalog.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_active':
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Product
        exclude = ['data_changed', 'data_created', 'owner', 'is_published']

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        excludes = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

        if cleaned_data in excludes:
            raise forms.ValidationError('Указаны запрещенные слова в названии')

        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        excludes = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

        if cleaned_data in excludes:
            raise forms.ValidationError('Указаны запрещенные слова в названии')

        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        exclude = ['product']


class ModeratorForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category']

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        excludes = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

        if cleaned_data in excludes:
            raise forms.ValidationError('Указаны запрещенные слова в названии')

        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        excludes = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

        if cleaned_data in excludes:
            raise forms.ValidationError('Указаны запрещенные слова в названии')

        return cleaned_data
