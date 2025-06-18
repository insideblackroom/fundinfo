from django.db import models
from fundinfo.common.models import BaseModel

class CorpInfo(BaseModel):
    assets = models.PositiveBigIntegerField(default=0)
    debts = models.PositiveBigIntegerField(default=0)
    
