from fundinfo.common.models import BaseModel
from django.db import models
from fundinfo.users.models import BaseUser
from fundinfo.core.models import Product

class Invoice(BaseModel):
    invoice_number = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(BaseUser, on_delete=models.PROTECT)
    description = models.TextField(null=True, blank=True)
    total = models.IntegerField()
    discount = models.FloatField(default=0)
    address = models.CharField(max_length=255)
    vat = models.FloatField(default=0.09)

    def __str__(self):
        return f"invoice nr. {self.invoice_number}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
        indexes = [
            models.Index(fields=['invoice_number']),
            models.Index(fields=['total']),
        ]

class InvoiceItem(BaseModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    count = models.IntegerField()
    price = models.IntegerField()
    discount = models.FloatField()
    total = models.IntegerField()
    