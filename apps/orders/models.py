import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('accepted', _('Accepted')),
        ('processing', _('Processing')),
        ('shipped', _('Shipped')),
        ('delivered', _('Delivered')),
        ('completed', _('Completed')),
        ('rejected', _('Rejected')),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='placed_orders')
    store = models.ForeignKey('stores.Store', on_delete=models.CASCADE, related_name='received_orders')
    status = models.CharField(_('Order Status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(_('Total Amount'), max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    @property
    def order_number(self):
        """
        تحويل أول جزء من الـ UUID (8 حروف) إلى رقم عشري ليكون رقم الطلب
        سيستخدم الفرونت إند نفس المنطق لضمان التناسق
        """
        first_part = str(self.id).split('-')[0]
        # تحويل أول 4 حروف من الـ Hex إلى Integer ليعطي رقم من 4-5 خانات
        return int(first_part[:4], 16)

    def __str__(self):
        return f"Order #{self.order_number} - {self.status}"

class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='order_items')
    variant = models.ForeignKey('products.ProductVariant', on_delete=models.CASCADE)
    quantity = models.IntegerField(_('Quantity'))
    price_at_order = models.DecimalField(_('Price at Order'), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

class OrderRating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='rating')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='given_ratings')
    store = models.ForeignKey('stores.Store', on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField(_('Rating'), choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(_('Comment'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Order Rating')
        verbose_name_plural = _('Order Ratings')

    def __str__(self):
        return f"Rating for Order {self.order.id} - {self.rating} stars"
