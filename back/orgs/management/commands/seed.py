from django.core.management.base import BaseCommand
from orgs.models import FinancialOrg, License

class Command(BaseCommand):
    help = "Seed demo data for FinCat"

    def handle(self, *args, **kwargs):
        # Лицензии
        l1, _ = License.objects.get_or_create(code="LIC-001")
        l2, _ = License.objects.get_or_create(code="LIC-002")
        l3, _ = License.objects.get_or_create(code="LIC-003")
        l4, _ = License.objects.get_or_create(code="LIC-004")
        l5, _ = License.objects.get_or_create(code="LIC-005")

        licenses = [l1, l2, l3, l4, l5]

        data = [
            ("АО «Народный Банк Казахстана» (Halyk Bank)", "970740000001", [l1]),
            ("АО «Kaspi Bank»", "050540000002", [l1]),
            ("АО «ForteBank»", "010140000003", [l1]),
            ("АО «Сбербанк Казахстан»", "060640000004", [l1]),
            ("АО «Alatau city Bank»", "080840000005", [l1, l4]),
            ("АО «Bank RBK»", "090940000006", [l1]),
            ("АО «Евразийский банк»", "030340000007", [l1]),
            ("АО «Банк ЦентрКредит»", "020240000008", [l1]),
            ("АО «Альфа-Банк Казахстан»", "070740000009", [l1]),
            ("АО «Банк Астана»", "120240000010", [l1]),
            ("АО «Шинхан Банк Казахстан»", "130340000011", [l1]),
            ("АО «Kassa Nova Bank»", "140440000012", [l1, l2]),
            ("АО «Microfinance Organization OnlineKazFinance»", "150540000013", [l2]),
            ("ТОО «МФО КазМикроФинанс»", "160640000014", [l2]),
            ("АО «Казахинстрах»", "170740000015", [l3]),
            ("АО «Номад Иншуранс»", "180840000016", [l3]),
            ("АО «Халык-Life»", "190940000017", [l3, l5]),
            ("АО «Freedom Finance»", "200140000018", [l4]),
            ("АО «Банк Отбасы»", "210240000019", [l1]),
            ("АО «ЕНПФ» (Единый накопительный пенсионный фонд)", "220340000020", [l5]),
        ]

        for name, bin_, lic_list in data:
            org, _ = FinancialOrg.objects.get_or_create(name=name, bin=bin_)
            org.licenses.set(lic_list)

        self.stdout.write(self.style.SUCCESS(f"✅ Seeded {len(data)} orgs & {len(licenses)} licenses"))
