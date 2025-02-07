from django import forms
import datetime


class StocktakingSettingsForm(forms.Form):
    department_name = forms.CharField(label="назва установи", max_length=100,
                                      initial='ВІЙСЬКОВА ЧАСТИНА ')
    edrpo_code = forms.CharField(label="Код ЭДРПОУ", max_length=30)
    document_date_number = forms.CharField(
        label="Дата і номер розпорядчого документу (Наказу)", max_length=300,
        initial='На підставі наказу командира в/ч А4548 від 27.09.21р.№237 виконано знімання фактичних залишків')
    date = forms.CharField(label="Дата описів, відомостей, актів", max_length=30,
                           initial='«11» листопада 2024 р.')
    date_remains = forms.CharField(label="Зняття залишків станом на", max_length=30,
                                   initial='10 листопада 2024 р.')
    start_date = forms.CharField(label="розпочата", max_length=30,
                                 initial='17 грудня 2024 року')
    end_date = forms.CharField(label="закінчена", max_length=30,
                               initial='22 грудня 2024 року')
    committee_chief = forms.CharField(label="Голова комісії", max_length=200)
    committee_members = forms.CharField(label="Члени комісії", widget=forms.Textarea())


class Appdx47SettingsForm(forms.Form):
    end_date = forms.DateField(label="Кінцева дата",
                               initial=datetime.date.today)
