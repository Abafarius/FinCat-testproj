from django.core.management.base import BaseCommand
from orgs.models import FinancialOrg, License

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        l1,_ = License.objects.get_or_create(code="LIC-001")
        l2,_ = License.objects.get_or_create(code="LIC-002")
        data = [
            ("АО Банк «А»","123456789012",[l1]),
            ("АО МФО «Б»","987654321000",[l1,l2]),
        ]
        for name, bin_, ls in data:
            org,_ = FinancialOrg.objects.get_or_create(name=name, bin=bin_)
            org.licenses.set(ls)
        self.stdout.write(self.style.SUCCESS("Seeded"))
