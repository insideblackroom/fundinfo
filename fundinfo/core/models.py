from django.db import models
from fundinfo.common.models import BaseModel
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth import get_user_model
# timezone aware
from django.utils import timezone
import uuid
import os

User = get_user_model()

def _get_upload_path(obj, filename):
    now = timezone.now()
    base_path = "pic"
    file_name = uuid.uuid5(uuid.NAMESPACE_URL, str(obj.pk))
    ext = os.path.splitext(filename)[1]
    path = os.path.join(base_path, now.strftime("%Y/%m"), f"{file_name}.{ext}")
    return path

class Base(BaseModel):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    deleted = models.BooleanField(default=False)
    delete_data = models.DateTimeField(default=None, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    
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
    description = models.TextField(null=True, blank=True, default="")
    price = models.IntegerField(default=0)
    discount = models.FloatField(default=0)
    enabled = models.BooleanField(default=True)
    # status = models.IntegerField(max_length=10, choices=STATUS_CHOICES, default=STATUS_ENABLED) 
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='products')
    # old_category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='old_producs')
    image = models.ImageField(upload_to=_get_upload_path)
    
    def get_absolute_url(self):
        return reverse('core:product_detail', args=[self.id])

    def __str__(self):
        return f"{self.name}"

class Category(Base):
    name = models.CharField(max_length=255)
    # product_set => products
    # old_products
    parent = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, blank=True, default=None, related_name='childs')

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

