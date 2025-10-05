from django.db import models
from users.models import User
from decimal import Decimal
from urllib.parse import quote_plus

CATEGORY_CHOICES = [
    ('Programming', 'Programming'),
    ('Design', 'Design'),
    ('Marketing', 'Marketing'),
    ('Business', 'Business'),
]

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
]

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.PositiveIntegerField(help_text="Duration in hours")
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    # New: whether the course is online
    online = models.BooleanField(default=False)
    # Price in INR (auto-calculated from `fee` using a simple fixed rate for now)
    price_inr = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    # Image URL (auto-generated placeholder if not provided)
    image_url = models.URLField(blank=True, default='')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-calculate price_inr if fee is set
        try:
            # Simple fixed conversion rate (1 unit of fee -> 82 INR). Replace with real rate if needed.
            rate = Decimal('82')
            if self.fee is not None:
                self.price_inr = (Decimal(self.fee) * rate).quantize(Decimal('0.01'))
        except Exception:
            # keep existing price_inr on error
            pass

        # Auto-generate a placeholder image URL based on the title if none provided
        if not self.image_url and self.title:
            text = quote_plus(self.title)
            self.image_url = f'https://via.placeholder.com/600x400.png?text={text}'

        super().save(*args, **kwargs)
