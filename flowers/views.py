from django.shortcuts import get_object_or_404, render

from .models import Bouquet


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


def order(request):
    # будущий код
    return render(request, "order.html")


def order_step(request):
    # будущий код
    return render(request, "order-step.html")


def quiz(request):
    # будущий код
    return render(request, "quiz.html")


def quiz_step(request):
    # будущий код
    return render(request, "quiz-step.html")


def result(request):
    # будущий код
    return render(request, "result.html")
