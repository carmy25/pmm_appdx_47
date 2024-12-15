from django import forms


class StocktakingSettingsForm(forms.Form):
    department_name = forms.CharField(label="назва установи", max_length=100)
    edrpo_code = forms.CharField(label="Код ЭДРПОУ", max_length=30)
    document_date_number = forms.CharField(
        label="Дата і номер розпорядчого документу (Наказу)", max_length=30)
    date = forms.CharField(label="Дата описів, відомостей, актів", max_length=30)
    date_remains = forms.CharField(label="Зняття залишків станом на", max_length=30)
    start_date = forms.CharField(label="розпочата", max_length=30)
    end_date = forms.CharField(label="закінчена", max_length=30)
    committee_chief = forms.CharField(label="Голова комісії", max_length=100)
    committee_members = forms.CharField(label="Члени комісії", widget=forms.Textarea())
