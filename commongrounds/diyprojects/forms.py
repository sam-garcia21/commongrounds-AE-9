from django import forms
from .models import Project, Favorite

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title',
            'category',
            'profile',
            'description',
            'materials',
            'steps',
        ]

class ProjectUpdateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title',
            'category',
            'description',
            'materials',
            'steps',
        ]