from django import forms
from django.forms import modelformset_factory, BaseModelFormSet, HiddenInput

from .models import Commission, Job

# class HiddenDeleteFormSet(BaseModelFormSet):
#     def add_fields(self, form, index):
#         super().add_fields(form, index)
#         form.fields['DELETE'].widget = HiddenInput()

JobFormSet = modelformset_factory(
    Job, 
    fields=['role', 'manpower_required'], 
    # formset=HiddenDeleteFormSet, 
    can_delete=True,
    extra=3
)

class CommissionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Commission
        exclude = ['maker']