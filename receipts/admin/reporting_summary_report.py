from django.http import HttpResponse
from receipts.forms import MyActionForm

from django.contrib import admin
from admin_object_actions.admin import ModelAdminObjectActionsMixin

from ..models.reporting import Reporting


class ReportingInline(admin.TabularInline):
    model = Reporting
    show_change_link = True
    # readonly_fields = ['number', 'start_date', 'end_date',]

    def has_change_permission(self, request, obj):
        return False

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj):
        return False


class ReportingSummaryReportAdmin(ModelAdminObjectActionsMixin, admin.ModelAdmin):
    inlines = [ReportingInline]
    search_fields = ['number']
    list_display = ['number', 'start_date',
                    'end_date', 'display_object_actions_list',]
    readonly_fields = (
        'display_object_actions_detail',
    )

    object_actions = [
        {
            'slug': 'gen-xlsx',
            'verbose_name': 'Згенерувати XSLX',
            'verbose_name_past': 'XSLX згенеровано',
            'form_class': MyActionForm,
            'fields': ('id', 'confirm'),
            'readonly_fields': ('id',),
            'permission': 'change',
        },
        {
            'slug': 'myotheraction',
            'verbose_name': 'my other action',
            'verbose_name_past': 'acted upon',
            'form_method': 'GET',
            'function': 'do_other_action',
        },

    ]

    def do_other_action(self, obj, form):
        return HttpResponse(content="ddd")

    def display_object_actions_detail(self, obj):
        return super().display_object_actions_detail(obj)
    display_object_actions_detail.short_description = 'Дії'
