from .models import Shop


def shops(request):
    return {"shops": Shop.objects.all()}
