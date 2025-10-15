from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User

# ===== BANQUET MODEL =====
class Banquet(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # Proper owner link
    owner_name = models.CharField(max_length=100)
    banquet_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    capacity = models.IntegerField()
    location = models.CharField(max_length=255)
    google_link = models.URLField(blank=True, null=True)
    services = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.banquet_name


# ===== VENUE MODEL (owners can list venues) =====
class Venue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='venues')
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# ===== BANQUET IMAGES =====
class BanquetImage(models.Model):
    banquet = models.ForeignKey(Banquet, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='banquet_images/')

    def __str__(self):
        return f"{self.banquet.banquet_name} Image"

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="150" height="100" />')
        return "No Image"
    image_tag.short_description = 'Image Preview'

# ===== SCHEDULE CALL MODEL =====
class ScheduleCall(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date = models.DateField()
    time_slot = models.CharField(max_length=50)
    reason = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.date}"

# ===== CONTACT MESSAGE MODEL =====
class ContactMessage(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)  # optional
    subject = models.CharField(max_length=50)
    message = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.subject}"
