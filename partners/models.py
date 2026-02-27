from django.db import models


class Supplier(models.Model):
    name       = models.CharField(max_length=200)
    email      = models.EmailField(blank=True)
    phone      = models.CharField(max_length=30, blank=True)
    address    = models.TextField(blank=True)
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'

    def __str__(self):
        return self.name


class Customer(models.Model):
    name       = models.CharField(max_length=200)
    email      = models.EmailField(blank=True)
    phone      = models.CharField(max_length=30, blank=True)
    address    = models.TextField(blank=True)
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
    def __str__(self):
        return self.name