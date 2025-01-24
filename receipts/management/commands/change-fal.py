from django.core.management.base import BaseCommand
import csv
import sys
from departments.models import Department
from fals.models import FAL, FALType
from receipts.models import ReceiptRequest, ReceiptRequestCoupon


class Command(BaseCommand):
    help = "Change fal in all documents"

    def add_arguments(self, parser):
        parser.add_argument("old_fal")
        parser.add_argument("new_fal")

    def handle(self, *args, **options):
        old_fal_name = options['old_fal']
        new_fal_name = options['new_fal']
        old_fal = FALType.objects.get(name=old_fal_name)
        for fe in old_fal.fals.all():
            fe.fal_type = FALType.objects.get(name=new_fal_name)
            fe.save()
