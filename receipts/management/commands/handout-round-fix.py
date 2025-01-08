from django.core.management.base import BaseCommand
from receipts.models.handout_list import HandoutList


class Command(BaseCommand):
    help = "Replace latin A with ukrainian"

    def handle(self, *args, **options):
        for h in HandoutList.objects.all():
            for f in h.fals.all():
                amount = f.amount
                f.amount = f.get_amount_rounded()
                f.save()
                print(f'f{f.fal_type.name}: before [{amount}], after [{f.amount}] ')
