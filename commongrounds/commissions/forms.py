from django import forms
from django.forms import modelformset_factory
from .models import Commission, Job, JobApplication

JobFormSet = modelformset_factory(
    Job,
    fields=['role', 'manpower_required',],
    can_delete=True,
    extra=0
)


class CommissionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Commission
        exclude = ['maker']


class JobApplicationForm(forms.ModelForm):

    class Meta:
        model = JobApplication
        fields = '__all__'
