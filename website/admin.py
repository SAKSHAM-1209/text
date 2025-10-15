from django.contrib import admin
from .models import Banquet, BanquetImage, ScheduleCall, ContactMessage
from django.utils.html import mark_safe

# ===== BANQUET IMAGES INLINE =====
class BanquetImageInline(admin.TabularInline):
    model = BanquetImage
    extra = 1
    readonly_fields = ('image_tag',)  # shows image preview
    fields = ('image', 'image_tag')

# ===== BANQUET ADMIN =====
@admin.register(Banquet)
class BanquetAdmin(admin.ModelAdmin):
    list_display = ('banquet_name', 'owner', 'owner_name', 'email', 'phone', 'capacity', 'location')
    inlines = [BanquetImageInline]

# ===== BANQUET IMAGE ADMIN =====
@admin.register(BanquetImage)
class BanquetImageAdmin(admin.ModelAdmin):
    list_display = ('banquet', 'image_tag')
    readonly_fields = ('image_tag',)

# ===== SCHEDULE CALL ADMIN =====
@admin.register(ScheduleCall)
class ScheduleCallAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'date', 'time_slot', 'reason', 'created_at')
    list_filter = ('date',)
    search_fields = ('name', 'email', 'phone')

# ===== CONTACT MESSAGE ADMIN =====
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'subject', 'created_at')
    search_fields = ('full_name', 'email', 'subject')
