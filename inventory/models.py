from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Category(models.Model):
    name        = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']
        verbose_name = 'Category'

    def __str__(self):
        return self.name


class Product(models.Model):
    sku           = models.CharField(max_length=50, unique=True, db_index=True)
    name          = models.CharField(max_length=200)
    description   = models.TextField(blank=True)
    category      = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')

    unit_cost     = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'),
                                        validators=[MinValueValidator(Decimal('0.00'))])
    unit_price    = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'),
                                        validators=[MinValueValidator(Decimal('0.00'))])

    stock         = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=0)

    is_active     = models.BooleanField(default=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'products'
        ordering = ['name']
        verbose_name = 'Product'

    def __str__(self):
        return f"{self.sku} — {self.name}"

    @property
    def inventory_value(self):
        return self.stock * self.unit_cost

    @property
    def is_low_stock(self):
        return self.stock <= self.reorder_level

    @property
    def stock_status(self):
        if self.stock <= self.reorder_level:
            return 'critical'
        if self.stock <= self.reorder_level * 1.5:
            return 'warning'
        return 'ok'