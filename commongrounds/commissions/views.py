from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Commission, JobApplication


class CommissionDetailView(DetailView):
    model = Commission
    template_name = "commission_detail.html"


class CommissionListView(ListView):
    model = Commission
    template_name = "commission_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.request.user, 'profile'):
            profile = self.request.user.profile
        if self.request.user.is_authenticated:
            context['logged_in'] = True
            commissions_applied_ids = [
                application.job.commission.id for application in JobApplication.objects.filter(applicant=profile)]
            context['all_commissions_list'] = Commission.objects.exclude(
                maker=profile).exclude(id__in=commissions_applied_ids)
            context['created_commissions_list'] = Commission.objects.filter(
                maker=profile)
            context['applied_commissions_list'] = Commission.objects.filter(
                id__in=commissions_applied_ids)
        else:
            context['logged_in'] = False
            context['all_commissions_list'] = Commission.objects.all()
        return context