import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.project.settings')
django.setup()

from decimal import Decimal
import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.apps.retail.models import RetailPoint, Employee
from core.apps.catalog.models import Product
from core.apps.inventory.models import Inventory

fake = Faker('ru_RU')
User = get_user_model()

DEALERS_COUNT = 20
PRODUCTS_COUNT = 30
EMPLOYEES_PER_DEALER = 2
MIN_PRODUCTS_PER_DEALER = 3
MAX_PRODUCTS_PER_DEALER = 10
MIN_STOCK = 0
MAX_STOCK = 20
MIN_PRICE = 10_000
MAX_PRICE = 100_000
MIN_REVENUE = 0
MAX_REVENUE = 50_000
PASSWORD = '123'

ELECTRONICS_BRANDS = [
    'Samsung', 'Apple', 'Xiaomi', 'Huawei', 'Sony', 'LG', 'Honor', 'JBL',
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Головной отдел
        head, created = RetailPoint.objects.get_or_create(
            point_type='head',
            defaults={
                'name': 'Головной отдел',
                'country': 'Россия',
                'city': fake.city(),
                'street': fake.street_name(),
                'house_number': fake.building_number(),
            }
        )
        if created:
            head_user = User.objects.create_user(
                username='head', password=PASSWORD, is_active=True, email=fake.email()
            )
            Employee.objects.create(
                user=head_user, retail_point=head,
                last_name=fake.last_name(), first_name=fake.first_name(),
                phone=fake.phone_number()[:16],
            )

        # Продукты
        products = []
        for _ in range(PRODUCTS_COUNT):
            p = Product.objects.create(
                brand=random.choice(ELECTRONICS_BRANDS),
                model=fake.bothify('Model ?##'),
                price=Decimal(random.randint(MIN_PRICE, MAX_PRICE)),
                release_date=fake.date_between(start_date='-2y', end_date='today'),
            )
            products.append(p)

        # Дилеры
        for _ in range(DEALERS_COUNT):
            dealer = RetailPoint.objects.create(
                name=f'Дилерский центр {fake.city()}',
                point_type='dealer',
                country='Россия',
                city=fake.city(),
                street=fake.street_name(),
                house_number=fake.building_number(),
                daily_revenue=Decimal(random.randint(MIN_REVENUE, MAX_REVENUE)),
            )
            for _ in range(EMPLOYEES_PER_DEALER):
                user = User.objects.create_user(
                    username=fake.user_name(), password=PASSWORD, is_active=True, email=fake.email(),
                )
                Employee.objects.create(
                    user=user, retail_point=dealer,
                    last_name=fake.last_name(), first_name=fake.first_name(),
                    phone=fake.phone_number()[:16],
                )

            for product in random.sample(products, random.randint(MIN_PRODUCTS_PER_DEALER, MAX_PRODUCTS_PER_DEALER)):
                Inventory.objects.create(
                    product=product, retail_point=dealer,
                    quantity=random.randint(MIN_STOCK, MAX_STOCK),
                )

        total_employees = 1 + DEALERS_COUNT * EMPLOYEES_PER_DEALER
        print(f'Готово: 1 головной, {DEALERS_COUNT} дилеров, {PRODUCTS_COUNT} продуктов, {total_employees} сотрудников')

if __name__ == '__main__':
    cmd = Command()
    cmd.handle()
