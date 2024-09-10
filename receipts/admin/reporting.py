from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
import nested_admin

from receipts.models.reporting import Reporting, FALReportEntry


class FALReportEntry(admin.TabularInline):
    model = FALReportEntry
    autocomplete_fields = ['fal_type']


class ReportingAdmin(admin.ModelAdmin):
    inlines = [FALReportEntry]
