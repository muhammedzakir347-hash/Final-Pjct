from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Recitation

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username",)



class RecitationForm(forms.ModelForm):
    class Meta:
        model = Recitation
        fields = ["surah", "reciter", "audio_file", "recitation_type"]


class BulkTextForm(forms.Form):
    data = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 14, "placeholder": "Paste CSV lines here..."}),
        help_text="Paste CSV rows (one row per line)."
    )