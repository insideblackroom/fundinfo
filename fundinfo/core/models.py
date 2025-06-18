from django.db import models
from fundinfo.common.models import BaseModel
from django.utils.text import slugify
import uuid
from users.models import BaseUser

class Base(BaseModel):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    deleted = models.BooleanField(default=False)
    delete_data = models.DateTimeField(default=None, null=True, blank=True)
    user = models.ForeignKey(BaseUser, on_delete=models.PROTECT)
    
    class Meta:
        abstract = True

class Product(Base):
    # STATUS_ENABLED = 0
    # STATUS_DISABLED = 1
    # STATUS_DELETED = 2
    # STATUS_CHOICES = (
    #         (STATUS_ENABLED, "Enabled"),
    #         (STATUS_DISABLED, "Disabled"),
    #         (STATUS_DELETED, "Deleted")
    #         )
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    price = models.IntegerField(default=0)
    discount = models.FloatField(default=0)
    enabled = models.BooleanField(default=True)
    # status = models.IntegerField(max_length=10, choices=STATUS_CHOICES, default=STATUS_ENABLED) 
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='products')
    old_category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='old_producs')

    def __str__(self):
        return f"{self.name}"

class Category(Base):
    name = models.CharField(max_length=255)
    # product_set => products
    # old_products
    parent = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, default=None, related_name='childs')

    def __str__(self):
        return f"{self.name}"
        
class Tag(Base):
    name = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.name}"

class Comment(Base):
    name = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.name}"

class Like(Base):
    ...

