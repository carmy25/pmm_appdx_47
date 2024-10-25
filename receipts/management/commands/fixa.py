from django.core.management.base import BaseCommand
from receipts.models.receipt import ReceiptRequest, ReceiptRequestCoupon


class Command(BaseCommand):
    help = "Replace latin A with ukrainian"

    def handle(self, *args, **options):
        for r in list(ReceiptRequest.objects.all()) + list(
            ReceiptRequestCoupon.objects.all()
        ):
            old_sender = r.sender
            old_dest = r.destination
            r.sender = r.sender.replace("A", "А")
            r.destination = r.destination.replace("A", "А")
            r.sender = r.sender.replace("a", "А")
            r.destination = r.destination.replace("a", "А")
            r.sender = r.sender.replace("а", "А")
            r.destination = r.destination.replace("а", "А")
            if r.sender != old_sender or r.destination != old_dest:
                r.save()
                self.stdout.write(
                    self.style.SUCCESS('Successfully replaced "%s"' % r.id)
                )
