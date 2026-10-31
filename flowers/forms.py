from django import forms

from .models import ConsultationRequest


class ConsultationRequestForm(forms.ModelForm):
    class Meta:
        model = ConsultationRequest
        fields = ("client_name", "client_phone")
