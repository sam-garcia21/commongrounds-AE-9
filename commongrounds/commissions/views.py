from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

from .models import Commission, Job, JobApplication
from .forms import CommissionForm, JobFormSet
from .services import create_commission


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


class CommissionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = '/accounts/login/'

    model = Commission
    template_name = 'commission_create.html'
    form_class = CommissionForm

    def test_func(self):
        if (self.request.user.profile.role == 'Commission Maker'):
            return True
        return False

    def get_initial(self):
        return {'maker': self.request.user}

    def get_context_data(self, **kwargs):
        self.object = None
        context = super().get_context_data(**kwargs)
        context['formset'] = JobFormSet(
            queryset=Job.objects.none(), prefix='job-form')
        return context

    def post(self, request, *args, **kwargs):
        commission = CommissionForm(request.POST)
        job_formset = JobFormSet(
            request.POST, request.FILES, prefix='job-form')
        for job in job_formset:
            print(job.data.get('DELETE'))

        if commission.is_valid() and job_formset.is_valid():
            new_commission = create_commission(author=request.user.profile,
                              data=commission.cleaned_data, jobs_data=job_formset.cleaned_data)
            return redirect(new_commission.get_absolute_url())

        return self.render_to_response(self.get_context_data(formset=job_formset))

    def get_success_url(self):
        return reverse_lazy('commissions:commission_detail', kwargs={'pk': self.object.commission.pk})
