from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        IN     = 'IN',     'Purchase (IN)'
        OUT    = 'OUT',    'Sale (OUT)'
        ADJUST = 'ADJUST', 'Adjustment'

    class Status(models.TextChoices):
        PENDING   = 'pending',   'Pending'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    reference  = models.CharField(max_length=20, unique=True, editable=False)
    type       = models.CharField(max_length=10, choices=TransactionType.choices)
    product    = models.ForeignKey('inventory.Product',  on_delete=models.PROTECT, related_name='transactions')
    supplier   = models.ForeignKey('partners.Supplier',  on_delete=models.SET_NULL, null=True, blank=True)
    customer   = models.ForeignKey('partners.Customer',  on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey('accounts.User',      on_delete=models.SET_NULL, null=True)

    quantity   = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_cost  = models.DecimalField(max_digits=12, decimal_places=2,
                                     validators=[MinValueValidator(Decimal('0.00'))])
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    notes      = models.TextField(blank=True)
    status     = models.CharField(max_length=10, choices=Status.choices, default=Status.COMPLETED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.reference} — {self.type} — {self.product.name}"

    @property
    def total_amount(self):
        if self.type == self.TransactionType.OUT:
            return self.quantity * self.unit_price
        return self.quantity * self.unit_cost

    def save(self, *args, **kwargs):
        if not self.reference:
            last = Transaction.objects.order_by('-id').first()
            next_id = (last.id + 1) if last else 1
            self.reference = f"TXN-{next_id:04d}"
        super().save(*args, **kwargs)