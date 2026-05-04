from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import Event, EventSignup
from .forms import EventForm, EventSignupForm


def event_list(request):
    all_events = Event.objects.all()
    created_events = []
    signed_events = []
    if request.user.is_authenticated:
        profile = request.user.profile
        created_events = Event.objects.filter(organizer=profile)
        signed_events = signed_events = Event.objects.filter(
            signups__user_registrant=profile).distinct()
        all_events = all_events.exclude(signups__user_registrant=profile)
        all_events = all_events.exclude(organizer=profile)
    return render(request, 'localevents/event_list.html', {
        'all_events': all_events,
        'created_events': created_events,
        'signed_events': signed_events,
    })


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    is_owner = False
    if request.user.is_authenticated:
        is_owner = event.organizer.filter(pk=request.user.profile.pk).exists()
    return render(request, 'localevents/event_detail.html', {
        'object': event,
        'signup_count': event.signups.count(),
        'is_owner': is_owner,
        'is_full': event.is_full(),
    })


@login_required
def event_create(request):
    if request.user.profile.role != 'Event Organizer':
        return redirect('localevents:event-list')
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer.set([request.user.profile])
            event.save()
            form.save_m2m()
            return redirect('localevents:event-detail', pk=event.pk)
    else:
        form = EventForm()
    return render(request, 'localevents/event_form.html', {'form': form})


@login_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if not event.organizer.filter(pk=request.user.profile.pk).exists():
        return redirect('localevents:event-detail', pk=event.pk)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            if event.is_full():
                event.status = 'Full'
            else:
                event.status = 'Available'
            event.save()
            return redirect('localevents:event-detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'localevents/event_form.html', {'form': form, 'event': event})


def event_signup(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        if request.user.is_authenticated:
            if event.organizer.filter(pk=request.user.profile.pk).exists():
                return redirect('localevents:event-detail', pk=pk)
            EventSignup.objects.get_or_create(
                event=event,
                user_registrant=request.user.profile,
                defaults={"new_registrant": ""}
            )
            return redirect('localevents:event-detail', pk=pk)
        else:
            form = EventSignupForm(request.POST)
            if form.is_valid():
                EventSignup.objects.create(
                    event=event,
                    new_registrant=form.cleaned_data["name"],
                    user_registrant=None
                )
                return redirect('localevents:event-detail', pk=pk)
    else:
        form = EventSignupForm()
    return render(request, 'localevents/event_signup.html', {
        'form': form,
        'event': event,
    })
