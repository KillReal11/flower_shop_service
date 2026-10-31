from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from flowers.models import Bouquet, BudgetInterval, ConsultationRequest, Event, Order, PromoCode

from .forms import ConsultationRequestForm


def index(request):
    bouquets = Bouquet.objects.filter(is_recommended=True).order_by("id")[:3]
    return render(request, "index.html", {"bouquets": bouquets})


def card(request, slug):
    bouquet = get_object_or_404(Bouquet, slug=slug)
    return render(request, "card.html", {"bouquet": bouquet})


def catalog(request):
    bouquets = Bouquet.objects.order_by("id")
    return render(request, "catalog.html", {"bouquets": bouquets})


def consultation(request):
    if request.method == "POST":
        form = ConsultationRequestForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data["client_phone"]
            already_waiting = ConsultationRequest.objects.filter(
                client_phone=phone, status="new"
            ).exists()
            if not already_waiting:
                form.save()
            messages.success(request, "Заявка отправлена! Мы скоро вам перезвоним.")
        else:
            messages.error(request, "Не удалось отправить заявку. Проверьте номер телефона.")
        return redirect(f"{reverse('index')}#consultation")

    form = ConsultationRequestForm()
    return render(request, "consultation.html", {"form": form})


def create_order(request, bouquet_id):
    bouquet = get_object_or_404(Bouquet, id=bouquet_id)

    if request.method == "POST":
        client_name = request.POST.get("fname", "").strip()
        client_phone = request.POST.get("tel", "").strip()
        delivery_address = request.POST.get("address", "").strip()
        delivery_time = request.POST.get("orderTime", "").strip()

        if not all([client_name, client_phone, delivery_address, delivery_time]):
            error_message = "Пожалуйста, заполните все поля формы доставки!"
            return render(
                request, "order.html", {"bouquet": bouquet, "error_message": error_message}
            )

        order = Order.objects.create(
            bouquet=bouquet,
            client_name=client_name,
            client_phone=client_phone,
            delivery_address=delivery_address,
            delivery_time=delivery_time,
            total_price=bouquet.price,
            status="new",
            is_paid=False,
        )

        return redirect("order_payment", order_id=order.id)

    return render(request, "order.html", {"bouquet": bouquet})


def order_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    promo_error = None
    payment_error = None

    if request.method == "POST":
        order.client_email = request.POST.get("email", "").strip()

        if "apply_promo" in request.POST:
            promo_code_text = request.POST.get("promocode", "").strip().upper()
            if promo_code_text:
                try:
                    promocode = PromoCode.objects.get(code=promo_code_text, is_active=True)
                    if promocode.valid_until and promocode.valid_until < timezone.now():
                        raise PromoCode.DoesNotExist
                    order.promocode = promocode
                    order.total_price = (
                        order.bouquet.price * (100 - promocode.discount_percentage) / 100
                    )
                    order.save()
                except PromoCode.DoesNotExist:
                    promo_error = "Промокод не существует или истек"
                    order.promocode = None
                    order.total_price = order.bouquet.price
                    order.save()

        elif "pay" in request.POST:
            card_num = request.POST.get("cardNum", "").strip()
            card_mm = request.POST.get("cardMm", "").strip()
            card_gg = request.POST.get("cardGg", "").strip()
            card_fname = request.POST.get("cardFname", "").strip()
            card_cvc = request.POST.get("cardCvc", "").strip()

            if not all([card_num, card_mm, card_gg, card_fname, card_cvc]):
                payment_error = "Пожалуйста, заполните все обязательные поля карты!"
            elif len(card_cvc) < 3 or len(card_num) < 16:
                payment_error = "Неверный формат номера карты или CVC-кода!"
            else:
                order.is_paid = True
                order.status = "accepted"
                order.save()
                return render(request, "thanks.html", {"order": order})

    return render(
        request,
        "order-step.html",
        {"order": order, "promo_error": promo_error, "payment_error": payment_error},
    )


def quiz_event(request):
    if request.method == "POST":
        event_id = request.POST.get("event_id")
        if not event_id:
            return redirect("quiz")
        request.session["quiz_event_id"] = event_id
        return redirect("quiz_step")

    events = Event.objects.all()
    return render(request, "quiz.html", {"events": events})


def quiz_budget(request):
    if "quiz_event_id" not in request.session:
        return redirect("quiz")

    if request.method == "POST":
        budget_id = request.POST.get("budget_id")
        if not budget_id:
            return redirect("quiz_step")
        request.session["quiz_budget_id"] = budget_id
        return redirect("result")

    budgets = BudgetInterval.objects.all()
    return render(request, "quiz-step.html", {"budgets": budgets})


def quiz_result(request):
    event_id = request.session.get("quiz_event_id")
    budget_id = request.session.get("quiz_budget_id")

    if not (event_id and budget_id):
        return redirect("quiz")

    budget = get_object_or_404(BudgetInterval, pk=budget_id)
    bouquet = Bouquet.objects.filter(
        events__id=event_id,
        price__gte=budget.min_price,
        price__lte=budget.max_price,
    ).first()

    request.session.pop("quiz_event_id", None)
    request.session.pop("quiz_budget_id", None)

    return render(request, "result.html", {"bouquet": bouquet})
