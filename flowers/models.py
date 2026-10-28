from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Event(models.Model):
    title = models.CharField("Название события", max_length=100)

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "События"

    def __str__(self):
        return self.title


class Bouquet(models.Model):
    title = models.CharField("Название букета", max_length=200)
    slug = models.SlugField("Слуг для URL", unique=True)
    description = models.TextField("Описание")
    meaning = models.TextField("Смысл букета")
    price = models.DecimalField(
        "Цена",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    image = models.ImageField("Фото букета", upload_to="bouquets/")
    events = models.ManyToManyField(
        Event,
        verbose_name="Подходит для событий",
        related_name="bouquets",
    )
    is_recommended = models.BooleanField("Рекомендованный", default=False)

    class Meta:
        verbose_name = "Букет"
        verbose_name_plural = "Букеты"

    def __str__(self):
        return self.title


class BudgetInterval(models.Model):
    title = models.CharField("Название интервала", max_length=100)
    min_price = models.DecimalField("Минимальная цена", max_digits=10, decimal_places=2, default=0)
    max_price = models.DecimalField(
        "Максимальная цена",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    sort_order = models.PositiveIntegerField("Порядок сортировки", default=0)

    class Meta:
        verbose_name = "Интервал бюджета"
        verbose_name_plural = "Интервалы бюджета"
        ordering = ["sort_order"]

    def __str__(self):
        return self.title


class PromoCode(models.Model):
    code = models.CharField("Промокод", max_length=50, unique=True)
    discount_percentage = models.PositiveIntegerField(
        "Скидка в процентах",
        validators=[MinValueValidator(1), MaxValueValidator(100)],
    )
    is_active = models.BooleanField("Активен", default=True)
    valid_until = models.DateTimeField("Действует до", blank=True, null=True)

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"

    def __str__(self):
        return f"{self.code} (-{self.discount_percentage}%)"


class Order(models.Model):
    STATUS_CHOICES = [
        ("new", "Новый"),
        ("accepted", "Принят флористом"),
        ("delivery", "В доставке"),
        ("completed", "Завершен"),
    ]

    bouquet = models.ForeignKey(
        Bouquet,
        verbose_name="Заказанный букет",
        on_delete=models.SET_NULL,
        null=True,
    )
    client_name = models.CharField("Имя клиента", max_length=100)
    client_phone = PhoneNumberField("Телефон клиента", region="RU")
    delivery_address = models.TextField("Адрес доставки")
    delivery_time = models.CharField("Время доставки", max_length=100)

    promocode = models.ForeignKey(
        PromoCode,
        verbose_name="Примененный промокод",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    total_price = models.DecimalField("Итоговая стоимость", max_digits=10, decimal_places=2)

    status = models.CharField("Статус заказа", max_length=20, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ #{self.id} от {self.client_name}"


class ConsultationRequest(models.Model):
    STATUS_CHOICES = [
        ("new", "Новая заявка"),
        ("processed", "Перезвонили"),
    ]

    client_name = models.CharField("Имя клиента", max_length=100, blank=True)
    client_phone = PhoneNumberField("Телефон для связи", region="RU")
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField("Дата заявки", auto_now_add=True)

    class Meta:
        verbose_name = "Заявка на консультацию"
        verbose_name_plural = "Заявки на консультации"

    def __str__(self):
        return f"Консультация для {self.client_phone} ({self.get_status_display()})"
