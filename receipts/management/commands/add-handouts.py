from django.core.management.base import BaseCommand
import openpyxl
import csv
from departments.models import Department
from fals.models import FAL, FALType
from receipts.models import HandoutList


class Command(BaseCommand):
    help = "Add handouts from summary reports"

    def add_arguments(self, parser):
        parser.add_argument("file")
        parser.add_argument("--fal", default='ДП-л-Євро5 В0')

    def handle(self, *args, **options):
        records = csv.reader(open(options['file']), delimiter='\t')
        fal_name = options['fal']
        breakpoint()
        for record in records:
            print(record)
            number, date_str, dep_name, _, amount = record
            hl = HandoutList(
                number=number,
                operation_date=date_str,
                sender=Department.objects.get(name='А4548'),
                destination=Department.objects.get(name=dep_name))
            hl.save()
            fal = FAL(fal_type=FALType.objects.get(name=fal_name),
                      amount=int(amount),
                      document_object=hl)
            fal.save()
            hl.fals.add(fal)
