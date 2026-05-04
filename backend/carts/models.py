from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

BULK_DISCOUNT_PERCENT = Decimal("5")


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart — {self.user.email}"

    @property
    def item_count(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        return sum(item.line_total for item in self.items.select_related("product"))

    @property
    def bulk_discount_eligible(self):
        return self.item_count > 1

    @property
    def discount_percent(self):
        return BULK_DISCOUNT_PERCENT if self.bulk_discount_eligible else Decimal("0")

    @property
    def discount_amount(self):
        if not self.bulk_discount_eligible:
            return Decimal("0")
        return (self.subtotal * BULK_DISCOUNT_PERCENT / Decimal("100")).quantize(
            Decimal("0.01")
        )

    @property
    def total(self):
        return self.subtotal - self.discount_amount


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = [["cart", "product"]]

    def __str__(self):
        return f"{self.cart.user.email} — {self.product.name} × {self.quantity}"

    @property
    def line_total(self):
        return self.product.price * self.quantity
