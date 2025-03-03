import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from receipts.models import ReceiptRequestCoupon
from pathlib import Path


class Command(BaseCommand):
    help = "Copy receipts scan to separate folder"

    def add_arguments(self, parser):
        parser.add_argument("start")
        parser.add_argument("end")
        parser.add_argument("dest")

    def handle(self, *args, **options):
        start = options['start']
        end = options['end']
        dest = options['dest']
        media = settings.MEDIA_ROOT
        for r in ReceiptRequestCoupon.objects.filter(
                operation_date__gt=start, operation_date__lt=end):
            if r.scan.name:
                src = media / r.scan.name
                dst = Path(dest) / f'{r.number}-{r.book_number}{r.book_series}.{r.sender}.pdf'
                print(f'copying {src} to {dst}')
                shutil.copyfile(src, dst)
