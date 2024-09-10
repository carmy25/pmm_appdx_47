from django.contrib import admin

from receipts.models.reporting import FALReportEntry


class FALReportEntry(admin.TabularInline):
    model = FALReportEntry
    autocomplete_fields = ['fal_type']


class ReportingAdmin(admin.ModelAdmin):
    inlines = [FALReportEntry]
    search_fields = ['number', 'department__name']
    list_display = ['department__name', 'start_date', 'end_date']
