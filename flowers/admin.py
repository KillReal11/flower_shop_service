from django.contrib import admin
from django.utils.html import mark_safe

from .models import (
    Bouquet,
    BudgetInterval,
    ConsultationRequest,
    Event,
    Order,
    PromoCode,
)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)


@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "is_recommended", "slug")
    list_filter = ("is_recommended", "events")
    search_fields = ("title", "description")
    list_editable = ("is_recommended",)
    filter_horizontal = ("events",)
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="max-width: 200px; max-height: 200px;" />'
            )
        return "Нет фото"

    image_preview.short_description = "Предпросмотр"


@admin.register(BudgetInterval)
class BudgetIntervalAdmin(admin.ModelAdmin):
    list_display = ("title", "min_price", "max_price", "sort_order")
    list_editable = ("sort_order",)
    ordering = ["sort_order"]


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "discount_percentage", "is_active", "valid_until")
    list_filter = ("is_active",)
    search_fields = ("code",)
    list_editable = ("is_active",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "client_name",
        "client_phone",
        "bouquet",
        "total_price",
        "status",
        "created_at",
        "is_paid",
    )
    list_filter = ("status", "created_at")
    search_fields = ("client_name", "client_phone", "delivery_address")
    readonly_fields = ("created_at",)
    ordering = ["-created_at"]
    list_editable = ("status",)


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "client_name", "client_phone", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("client_phone", "client_name")
    list_editable = ("status",)
    ordering = ["-created_at"]
    readonly_fields = ("created_at",)
