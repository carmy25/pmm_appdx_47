from django.core.management.base import BaseCommand
from pprint import pprint
from departments.models import Department
from fals.models import FAL, FALType
from receipts.models import HandoutList
from receipts.models.reporting import Reporting


class Command(BaseCommand):
    help = "Show reportings income summary by fal."

    def add_arguments(self, parser):
        parser.add_argument("--fal", default='ДП-л-Євро5 В0')

    def handle(self, *args, **options):
        fal_type = options['fal']
        reportings = Reporting.objects.filter(
            fals__fal_type__name=fal_type).order_by('end_date')
        for report in reportings:
            report.fals.get(fal_type__name=fal_type)
