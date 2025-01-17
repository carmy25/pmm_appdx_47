from django.core.management.base import BaseCommand
import csv
import sys
from departments.models import Department
from fals.models import FAL, FALType
from receipts.models import ReceiptRequest, ReceiptRequestCoupon


class Command(BaseCommand):
    help = "Print Income and Outcome for period"

    def add_arguments(self, parser):
        parser.add_argument("start")
        parser.add_argument("end")

    def handle(self, *args, **options):
        records = csv.writer(sys.stdout, delimiter=';')
        start = options['start']
        end = options['end']
        fals = {}
        for r in ReceiptRequestCoupon.objects.filter(
                operation_date__gt=start, operation_date__lt=end):
            for f in r.fals.all():
                if fals.get(f.fal_type):
                    fals[f.fal_type]['income'] += f.amount
                else:
                    fals[f.fal_type] = {'income': f.amount, 'outcome': 0}

        for r in ReceiptRequest.objects.filter(
                operation_date__gt=start, operation_date__lt=end):
            for f in r.fals.all():
                if fals.get(f.fal_type):
                    fals[f.fal_type]['outcome'] += f.amount
                else:
                    fals[f.fal_type] = {'outcome': f.amount, 'income': 0}

        for f, d in fals.items():
            records.writerow((f.name, d['income'], d['outcome']))
        sys.stdout.flush()
