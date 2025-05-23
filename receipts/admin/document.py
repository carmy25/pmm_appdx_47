from datetime import datetime
from django.contrib import admin
from django.db.models import Q
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType


from rangefilter.filters import DateRangeFilterBuilder

from nested_admin import NestedModelAdmin, NestedGenericTabularInline
from fals.models import FAL
from receipts.models.handout_list import HandoutList
from receipts.models.invoice import Invoice
from receipts.models.writing_off_act import WritingOffAct
from summary_reports.admin.actions import create_summary_report


from ..models import Certificate


class FALInline(NestedGenericTabularInline):
    model = FAL
    autocomplete_fields = ["fal_type"]


class ScanListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = "найвністю скану документу"

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "have_scan"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [
            ("scan_present", "Cкан документа присутній"),
            ("scan_absent", "Без скану документа"),
        ]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if queryset.model is Certificate:
            # TODO: add scan to Certificate
            return queryset
        scan_present_qs = queryset.exclude(scan__isnull=True).exclude(scan__exact="")
        if self.value() == "scan_present":
            return scan_present_qs
        if self.value() == "scan_absent":
            return queryset.filter(Q(scan__isnull=True) | Q(scan__exact=""))


class DocumentAdmin(NestedModelAdmin):
    inlines = [FALInline]
    search_fields = ["number", "sender", "destination", "fals__fal_type__name"]
    ordering = ["operation_date"]
    list_filter = (
        ScanListFilter,
        ("operation_date", DateRangeFilterBuilder()),
    )
    list_display = [
        "number",
        "book",
        "sender",
        "destination",
        "operation_date",
        "scan_present",
        "last_updated",
    ]

    def book(self, obj):
        if type(obj) in [Certificate, Invoice, HandoutList, WritingOffAct]:
            return ""
        return f"{obj.book_number}{obj.book_series.upper()}"

    book.short_description = "Книга"

    def last_updated(self, obj):
        le_obj = LogEntry.objects.filter(
            object_id=obj.id,
            content_type=ContentType.objects.get(
                model=obj._meta.object_name.lower(),
                app_label=obj._meta.app_label)).order_by('-action_time').first()
        return le_obj.action_time if le_obj else None

    last_updated.short_description = 'Востаннє Оновлено'

    def scan_present(self, obj):
        return "Так" if obj.scan.name else "Ні"

    scan_present.short_description = "Скан присутній"

    def save_model(self, request, obj, form, change):
        if type(getattr(obj, 'sender', None)) is str and type(obj.destination) is str:
            obj.sender = obj.sender.upper()
            obj.destination = obj.destination.upper()
        super().save_model(request, obj, form, change)


class HandoutListAdmin(DocumentAdmin):
    search_fields = [
        "number",
        "sender__name",
        "destination__name",
        "fals__fal_type__name",
    ]
    autocomplete_fields = ["sender", "destination"]
    actions = [create_summary_report]
