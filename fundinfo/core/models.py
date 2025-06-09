from django.db import models
from fundinfo.common.models import BaseModel
from django.utils.text import slugify
import uuid

class Product(BaseModel):
    # STATUS_ENABLED = 0
    # STATUS_DISABLED = 1
    # STATUS_DELETED = 2
    # STATUS_CHOICES = (
    #         (STATUS_ENABLED, "Enabled"),
    #         (STATUS_DISABLED, "Disabled"),
    #         (STATUS_DELETED, "Deleted")
    #         )
    name = models.CharField(max_length=255)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    slug = models.SlugField()
    description = models.TextField()
    price = models.IntegerField(default=0)
    discount = models.FloatField(default=0)
    enabled = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    # status = models.IntegerField(max_length=10, choices=STATUS_CHOICES, default=STATUS_ENABLED) 
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='products')
    old_category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='old_producs')

class Category(BaseModel):
    name = models.CharField(max_length=255)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    # product_set => products
    # old_products
    parent = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, default=None, related_name='childs')

