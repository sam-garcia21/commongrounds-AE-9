from django import forms
from .models import Event, EventSignup


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['organizer', 'created_on', 'updated_on']
        widgets = {
            'start_time': forms.TextInput(
                attrs={'type': 'datetime-local'}
            ),
            'end_time': forms.TextInput(
                attrs={'type': 'datetime-local'}
            )
        }


class EventSignupForm(forms.ModelForm):
    name = forms.CharField(max_length=255, label='Your Name')

    class Meta:
        model = EventSignup
        fields = []
