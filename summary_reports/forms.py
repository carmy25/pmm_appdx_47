from django import forms
from admin_object_actions.forms import AdminObjectActionForm
from django.http import HttpResponse

from .models import ReportingSummaryReport


class MyActionForm(AdminObjectActionForm):

    confirm = forms.BooleanField()

    class Meta:
        model = ReportingSummaryReport
        fields = ()

    def do_object_action(self):
        return HttpResponse(content="ddd")
