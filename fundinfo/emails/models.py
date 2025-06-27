from fundinfo.common.models import BaseModel
from django.db import models

class Email(BaseModel):
    class Status(models.TextChoices):
        READY = "READY", "Ready"
        SENDING = "SENDING", "Sending"
        SENT = "SENT", "Sent"
        FAILED = "FAILED", "Failed"

    status = models.CharField(
        max_length=10, 
        db_index=True, 
        choices=Status.choices,
        default=Status.READY
    )
    subject = models.CharField(max_length=255)
    to = models.EmailField()
    html = models.TextField()
    plain_text = models.TextField(blank=True, null=True)
    sent_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"target: {self.to}"