from django import forms
from .models import Project, ProjectReview, Favorite

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

class ProjectReviewForm(forms.ModelForm):
    class Meta:
        model = ProjectReview
        fields = '__all__'

class FavoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = [
            'project_status',
        ]