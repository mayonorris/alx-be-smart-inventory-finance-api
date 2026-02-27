from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decimal import Decimal
from inventory.models import Category, Product
from partners.models import Supplier, Customer
from transactions.models import Transaction
from transactions.services import process_transaction

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed the database with sample data for demo purposes'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # ── Users ─────────────────────────────────────────────────────────────
        admin, _ = User.objects.get_or_create(
            email='admin@example.com',
            defaults={'username': 'admin', 'role': 'admin'}
        )
        admin.set_password('password123')
        admin.save()

        staff, _ = User.objects.get_or_create(
            email='staff@example.com',
            defaults={'username': 'staff', 'role': 'staff'}
        )
        staff.set_password('password123')
        staff.save()
        self.stdout.write('  Users created')

        # ── Categories ────────────────────────────────────────────────────────
        electronics,  _ = Category.objects.get_or_create(name='Electronics')
        accessories,  _ = Category.objects.get_or_create(name='Accessories')
        cables,       _ = Category.objects.get_or_create(name='Cables')
        self.stdout.write('  Categories created')

        # ── Suppliers ─────────────────────────────────────────────────────────
        supplier1, _ = Supplier.objects.get_or_create(
            name='TechSupply Co',
            defaults={'email': 'contact@techsupply.com', 'phone': '123456789'}
        )
        supplier2, _ = Supplier.objects.get_or_create(
            name='GlobalParts Ltd',
            defaults={'email': 'sales@globalparts.com', 'phone': '987654321'}
        )
        self.stdout.write('  Suppliers created')

        # ── Customers ─────────────────────────────────────────────────────────
        Customer.objects.get_or_create(
            name='John Doe',
            defaults={'email': 'john@example.com', 'phone': '111222333'}
        )
        Customer.objects.get_or_create(
            name='Jane Smith',
            defaults={'email': 'jane@example.com', 'phone': '444555666'}
        )
        self.stdout.write('  Customers created')

        # ── Products ──────────────────────────────────────────────────────────
        products_data = [
            ('SKU-001', 'Wireless Mouse',     accessories,  '15.00', '29.99', 0, 20),
            ('SKU-002', 'Mechanical Keyboard', accessories, '45.00', '129.99', 0, 15),
            ('SKU-003', 'USB-C Cable',         cables,      '3.00',  '9.00',  0, 50),
            ('SKU-004', 'HDMI Cable 2m',       cables,      '5.00',  '8.00',  0, 30),
            ('SKU-005', 'Laptop Stand',        accessories,  '18.00', '39.99', 0, 10),
            ('SKU-006', '27" Monitor',         electronics, '180.00','349.99', 0, 15),
            ('SKU-007', 'USB Hub 4-Port',      accessories,  '12.00', '24.99', 0, 20),
            ('SKU-008', 'Webcam HD',           electronics,  '45.00', '89.99', 0, 12),
        ]

        products = {}
        for sku, name, cat, cost, price, stock, reorder in products_data:
            p, _ = Product.objects.get_or_create(
                sku=sku,
                defaults={
                    'name': name, 'category': cat,
                    'unit_cost': Decimal(cost),
                    'unit_price': Decimal(price),
                    'stock': stock,
                    'reorder_level': reorder,
                }
            )
            products[sku] = p
        self.stdout.write('  Products created')

        # ── Transactions ──────────────────────────────────────────────────────
        # Purchase stock for each product
        purchase_data = [
            ('SKU-001', 50,  '15.00', supplier1),
            ('SKU-002', 30,  '45.00', supplier1),
            ('SKU-003', 100, '3.00',  supplier2),
            ('SKU-004', 60,  '5.00',  supplier2),
            ('SKU-005', 20,  '18.00', supplier1),
            ('SKU-006', 15,  '180.00',supplier2),
            ('SKU-007', 40,  '12.00', supplier1),
            ('SKU-008', 10,  '45.00', supplier2),
        ]

        for sku, qty, cost, supplier in purchase_data:
            process_transaction({
                'type':      Transaction.TransactionType.IN,
                'product':   products[sku],
                'supplier':  supplier,
                'quantity':  qty,
                'unit_cost': Decimal(cost),
                'unit_price': Decimal('0.00'),
                'notes':     'Initial stock',
                'status':    Transaction.Status.COMPLETED,
            }, admin)

        # Record some sales
        sales_data = [
            ('SKU-001', 5,  '15.00', '29.99'),
            ('SKU-002', 2,  '45.00', '129.99'),
            ('SKU-003', 20, '3.00',  '9.00'),
            ('SKU-006', 3,  '180.00','349.99'),
        ]

        for sku, qty, cost, price in sales_data:
            process_transaction({
                'type':      Transaction.TransactionType.OUT,
                'product':   products[sku],
                'supplier':  None,
                'quantity':  qty,
                'unit_cost': Decimal(cost),
                'unit_price': Decimal(price),
                'notes':     'Sample sale',
                'status':    Transaction.Status.COMPLETED,
            }, admin)

        self.stdout.write('  Transactions created')
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
        self.stdout.write('  Login: admin@example.com / password123')
        self.stdout.write('  Login: staff@example.com / password123')