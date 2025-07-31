from django.db import models
from fundinfo.common.models import BaseModel
from fundinfo.invoices.models import Invoice

class Payment(BaseModel):
    class STATUS(models.TextChoices):
        PENDING = "PENDING", "Pending"
        DONE = "DONE", "Done"
        ERROR = "ERROR", "Error"

    invoice = models.OneToOneField(Invoice, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS.choices, default=STATUS.PENDING)
    total = models.IntegerField()
    ref = models.CharField(max_length=255)
    descrption = models.TextField()
    authority = models.CharField(max_length=255)
    user_ip = models.CharField(max_length=15)

    def __str__(self):
        return f"payment id: {self.id}"
        