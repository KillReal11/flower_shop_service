from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from flowers.models import Bouquet, Order, PromoCode


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
    # будущий код
    return render(request, "consultation.html")


def create_order(request, bouquet_id):
    bouquet = get_object_or_404(Bouquet, id=bouquet_id)
    
    if request.method == 'POST':
        client_name = request.POST.get('fname', '').strip()
        client_phone = request.POST.get('tel', '').strip()
        delivery_address = request.POST.get('address', '').strip()
        delivery_time = request.POST.get('orderTime', '').strip()
        
        if not all([client_name, client_phone, delivery_address, delivery_time]):
            error_message = "Пожалуйста, заполните все поля формы доставки!"
            return render(request, 'order.html', {'bouquet': bouquet, 'error_message': error_message})
            
        order = Order.objects.create(
            bouquet=bouquet,
            client_name=client_name,
            client_phone=client_phone,
            delivery_address=delivery_address,
            delivery_time=delivery_time,
            total_price=bouquet.price,
            status='new',
            is_paid=False
        )
        
        return redirect('order_payment', order_id=order.id)

    return render(request, 'order.html', {'bouquet': bouquet})


def order_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    promo_error = None
    payment_error = None

    if request.method == 'POST':
        order.client_email = request.POST.get('email', '').strip()

        if 'apply_promo' in request.POST:
            promo_code_text = request.POST.get('promocode', '').strip().upper()
            if promo_code_text:
                try:
                    promocode = PromoCode.objects.get(code=promo_code_text, is_active=True)
                    if promocode.valid_until and promocode.valid_until < timezone.now():
                        raise PromoCode.DoesNotExist
                    order.promocode = promocode
                    order.total_price = order.bouquet.price * (100 - promocode.discount_percentage) / 100
                    order.save()
                except PromoCode.DoesNotExist:
                    promo_error = "Промокод не существует или истек"
                    order.promocode = None
                    order.total_price = order.bouquet.price
                    order.save()

        elif 'pay' in request.POST:
            card_num = request.POST.get('cardNum', '').strip()
            card_mm = request.POST.get('cardMm', '').strip()
            card_gg = request.POST.get('cardGg', '').strip()
            card_fname = request.POST.get('cardFname', '').strip()
            card_cvc = request.POST.get('cardCvc', '').strip()
            
            if not all([card_num, card_mm, card_gg, card_fname, card_cvc]):
                payment_error = "Пожалуйста, заполните все обязательные поля карты!"
            elif len(card_cvc) < 3 or len(card_num) < 16:
                payment_error = "Неверный формат номера карты или CVC-кода!"
            else:
                order.is_paid = True
                order.status = 'accepted'
                order.save()
                return render(request, 'thanks.html', {'order': order})

    return render(request, 'order-step.html', {
        'order': order, 
        'promo_error': promo_error, 
        'payment_error': payment_error
    })


def quiz(request):
    # будущий код
    return render(request, "quiz.html")


def quiz_step(request):
    # будущий код
    return render(request, "quiz-step.html")


def result(request):
    # будущий код
    return render(request, "result.html")
