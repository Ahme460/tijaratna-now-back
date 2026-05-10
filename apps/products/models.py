import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

class Product(models.Model):
    STATUS_CHOICES = (
        ('in_stock', _('In Stock')),
        ('out_of_stock', _('Out of Stock')),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    store = models.ForeignKey('stores.Store', on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey('stores.Category', on_delete=models.SET_NULL, null=True, related_name='products')
    name = models.CharField(_('Product Name'), max_length=255)
    description = models.TextField(_('Product Description'), blank=True, null=True)
    image_url = models.URLField(_('Image URL'), blank=True, null=True)
    is_popular = models.BooleanField(_('Is Popular'), default=False)
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='in_stock')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size = models.CharField(_('Size/Variant'), max_length=100)
    price = models.DecimalField(_('Selling Price'), max_digits=10, decimal_places=2)
    cost = models.DecimalField(_('Purchase Cost'), max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(_('Stock Quantity'), default=0)
    sku = models.CharField(_('SKU'), max_length=100, unique=True)

    class Meta:
        verbose_name = _('Product Variant')
        verbose_name_plural = _('Product Variants')
        ordering = ['price']

    def __str__(self):
        return f"{self.product.name} - {self.size}"
