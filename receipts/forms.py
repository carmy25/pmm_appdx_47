from django import forms


class StocktakingSettingsForm(forms.Form):
    department_name = forms.CharField(label="назва установи", max_length=100)
