import sys
from django.core.management.base import BaseCommand
from pprint import pprint
import csv
from departments.models import Department
from fals.models import FAL, FALType
from receipts.models import HandoutList
from receipts.models.certificate import Certificate
from receipts.models.receipt import ReceiptRequest, ReceiptRequestCoupon
from receipts.models.reporting import Reporting


class Command(BaseCommand):
    help = "Show reportings income summary by fal."

    def add_arguments(self, parser):
        parser.add_argument("start")
        parser.add_argument("end")
        parser.add_argument("--fal", default='ДП-л-Євро5 В0')

    def handle(self, *args, **options):
        start = options['start']
        end = options['end']
        fal_type = options['fal']
        by_dep = {}
        by_month_income = {}
        by_month_outcome = {}
        writer = csv.writer(sys.stdout)

        reportings = Reporting.objects.filter(
            fals__fal_type__name=fal_type,
            end_date__lte=end,
            start_date__gte=start).order_by('end_date')
        for report in reportings:
            fal = report.fals.get(fal_type__name=fal_type)
            month = report.end_date.month
            if by_dep.get(report.department) is None:
                by_dep[report.department] = {i: 0 for i in range(1, 13)}

            by_dep[report.department][month] += fal.get_income_kgs()

        certificates = Certificate.objects.filter(
            fals__fal_type__name=fal_type,
            operation_date__lte=end,
            operation_date__gte=start,
        )
        for certificate in certificates:
            fal = certificate.fals.get(fal_type__name=fal_type)
            month = certificate.operation_date.month
            if by_month_income.get(month) is None:
                by_month_income[month] = 0
            by_month_income[month] += fal.amount

        rrcs = ReceiptRequestCoupon.objects.filter(
            fals__fal_type__name=fal_type,
            operation_date__lte=end,
            operation_date__gte=start,
        )
        for rrc in rrcs:
            fal = rrc.fals.get(fal_type__name=fal_type)
            month = rrc.operation_date.month
            if by_month_income.get(month) is None:
                by_month_income[month] = 0
            by_month_income[month] += fal.amount

        rrs = ReceiptRequest.objects.filter(
            fals__fal_type__name=fal_type,
            operation_date__lte=end,
            operation_date__gte=start,
        )
        for rr in rrs:
            fal = rr.fals.get(fal_type__name=fal_type)
            month = rr.operation_date.month
            if by_month_outcome.get(month) is None:
                by_month_outcome[month] = 0
            by_month_outcome[month] -= fal.amount

        for dep, data in by_dep.items():
            row = [dep.name] + list(range(1, 13))
            for m, v in data.items():
                row[m] = v
            writer.writerow(row)

        row = ['Прихід'] + [0 for a in range(12)]
        for m, v in by_month_income.items():
            row[m] = v
        writer.writerow(row)
        row = ['Видхід'] + [0 for a in range(12)]
        for m, v in by_month_outcome.items():
            row[m] = v
        writer.writerow(row)

        row = ['Склад'] + [0 for a in range(12)]
        for m, v in by_month_income.items():
            row[m] = v + (by_month_outcome.get(m) or 0)
            for dep, data in by_dep.items():
                for ms, v in data.items():
                    row[ms] = round(row[ms] - v, 1)
        writer.writerow(row)
