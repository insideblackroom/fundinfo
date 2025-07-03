from django.db import models
from fundinfo.common.models import BaseModel

class GateWay(BaseModel):
    class STATUS(models.TextChoices):
        WAITING = "WAITING", "Waiting"
        REDIRECT_TO_BANK = "REDIRECT_TO_BANK", "Redirect to bank"
        VERIFIED = "VERIFIED", "Verified"
        PAID = "PAID", "Paid"
        IN_BANK = "IN_BANK", "In_Bank"
        FAILED = "FAILED", "Failed"
        REVERSED = "REVERSED", "Reversed"

    ref_id = models.CharField(
        max_length=255, 
        unique=True,
        null=False,
        blank=False,
        verbose_name="Reference Number"    
    )
    extra_description = models.TextField(null=True, blank=True, verbose_name="Extra Description")
    status = models.CharField(max_length=20, null=False, blank=False, choices=STATUS.choices, verbose_name="Status")
    payment_local_key = models.CharField(max_length=255, null=False, blank=False, verbose_name="Payment Key")
    amount = models.CharField(max_length=10, null=False, blank=False, verbose_name="Amount")

    class Meta:
        verbose_name = "GateWay"

    def __str__(self):
        return f"{self.id}"
