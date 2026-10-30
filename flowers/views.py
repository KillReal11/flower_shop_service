from django.shortcuts import get_object_or_404, redirect, render

from .models import Bouquet, BudgetInterval, Event


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
    bouquet = Bouquet.objects.filter(events__id=event_id,
                                     price__gte=budget.min_price,
                                     price__lte=budget.max_price,
                                     ).first()

    request.session.pop("quiz_event_id", None)
    request.session.pop("quiz_budget_id", None)

    return render(request, "result.html", {"bouquet": bouquet})
