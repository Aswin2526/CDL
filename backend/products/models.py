from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify


class StoreSettings(models.Model):
    """Singleton store profile for single-vendor ChitraBazar."""

    name = models.CharField(max_length=200, default="ChitraBazar")
    tagline = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    class Meta:
        verbose_name = "Store settings"
        verbose_name_plural = "Store settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class PaintingMedium(models.TextChoices):
    OIL = "oil", "Oil"
    ACRYLIC = "acrylic", "Acrylic"
    WATERCOLOR = "watercolor", "Watercolor"
    MIXED = "mixed", "Mixed Media"
    PENCIL = "pencil", "Pencil / Graphite"
    DIGITAL = "digital", "Digital Print"
    OTHER = "other", "Other"


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    artist_name = models.CharField(max_length=120, blank=True)
    medium = models.CharField(
        max_length=20,
        choices=PaintingMedium.choices,
        default=PaintingMedium.OIL,
    )
    dimensions = models.CharField(
        max_length=80,
        blank=True,
        help_text="e.g. 24 × 36 in",
    )
    is_framed = models.BooleanField(default=False)
    year_created = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    stock = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    review_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["is_active", "is_featured"]),
            models.Index(fields=["price"]),
            models.Index(fields=["average_rating"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.name

    @property
    def in_stock(self):
        return self.stock > 0

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to="products/")
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"Image for {self.product.name}"
