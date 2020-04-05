from django import forms
from .models import BusModel

class CreateBusForm(forms.ModelForm):
    class Meta:
        model = BusModel
        exclude = ["owner","active", "permitted"]
        widgets = { "category": forms.Select(attrs={"class":"form-control-bus-reg"}),
                    "ksrtc_category": forms.Select(attrs={"class":"form-control-bus-reg"})}