from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from django.contrib.auth.decorators import login_required
from .models import Event, Booking
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.admin.views.decorators import staff_member_required


@login_required
def event_create(request):
    if request.method == 'POST':
        form = forms.EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, 'Event created successfully.')
            return redirect('home')
    else:
        form = forms.EventForm()
    return render(request, 'events/event_form.html', {'form': form})


@login_required
def my_event(request):
    if request.user.is_superuser:
        events = Event.objects.all()  # Superuser sees all events
    else:
        # Normal user sees only their events
        events = Event.objects.filter(created_by=request.user)
    return render(request, 'events/my_event.html', {'data': events})


# def event_update(request, event_id):
#     event = get_object_or_404(Event, id=event_id, created_by=request.user)
#     if request.method == 'POST':
#         form = forms.EventForm(request.POST, instance=event)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Event updated successfully.')
#             return redirect('my_event')
#     else:
#         form = forms.EventForm(instance=event)
#     return render(request, 'events/event_form.html', {'form': form})
@login_required
def event_update(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    # Check if the user is the event creator or a superuser
    if request.user == event.created_by or request.user.is_superuser:
        if request.method == 'POST':
            form = forms.EventForm(request.POST, instance=event)
            if form.is_valid():
                form.save()
                messages.success(request, 'Event updated successfully.')
                return redirect('my_event')
        else:
            form = forms.EventForm(instance=event)
    else:
        messages.error(
            request, 'You do not have permission to update this event.')
        return redirect('my_event')

    return render(request, 'events/event_form.html', {'form': form})


# @login_required
# def event_delete(request, event_id):
#     event = get_object_or_404(Event, id=event_id, created_by=request.user)
#     if request.method == 'POST':
#         event.delete()
#         messages.success(request, 'Event deleted successfully.')
#         return redirect('my_event')
#     return render(request, 'events/event_confirm_delete.html', {'event': event})
@login_required
def event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user == event.created_by or request.user.is_superuser:
        if request.method == 'POST':
            event.delete()
            messages.success(request, 'Event deleted successfully.')
            return redirect('my_event')
    else:
        messages.error(
            request, 'You do not have permission to delete this event.')
        return redirect('my_event')

    return render(request, 'events/event_confirm_delete.html', {'event': event})


@staff_member_required
def event_admin_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted by admin.')
        return redirect('my_event')
    return render(request, 'events/event_confirm_delete.html', {'event': event})


# @login_required
# def book_event(request, event_id):
#     event = get_object_or_404(Event, id=event_id)
#     if Booking.objects.filter(user=request.user, event=event).exists():
#         messages.warning(request, "You have already booked this event.")
#         return redirect('home')
#     booking = Booking(user=request.user, event=event)
#     booking.save()
#     messages.success(request, "You have successfully booked the event!")
#     return redirect('home')
@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if Booking.objects.filter(event=event).count() >= event.capacity:
        messages.warning(request, "This event is fully booked.")
        return redirect('home')
    if Booking.objects.filter(user=request.user, event=event).exists():
        messages.warning(request, "You have already booked this event.")
        return redirect('home')
    booking = Booking(user=request.user, event=event)
    booking.save()
    messages.success(request, "You have successfully booked the event!")
    return redirect('home')


@login_required
def booked_events(request):
    bookings = Booking.objects.filter(
        user=request.user).select_related('event')
    return render(request, 'events/booked_events.html', {'bookings': bookings})


@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
    messages.success(request, "Booking deleted successfully.")
    return redirect('booked_events')


def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = forms.RegisterForm(request.POST)
            if form.is_valid():
                messages.success(request, "User Created Successfully")
                form.save()
            else:
                print(form.errors)
        else:
            form = forms.RegisterForm()
        return render(request, 'signup.html', {'forms': form})
    else:
        return redirect('login')


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                name = form.cleaned_data['username']
                user_pass = form.cleaned_data['password']
                # is user is available in database
                user = authenticate(username=name, password=user_pass)
                if user is not None:
                    login(request, user)
                    print(user)
                    return redirect('home')
        else:
            form = AuthenticationForm()
            return render(request, 'login.html', {'forms': form})
    else:
        return redirect('home')
    return render(request, 'login.html', {'forms': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = forms.ChangeData(request.POST, instance=request.user)
            if form.is_valid():
                messages.success(request, "User Updated Successfully")
                form.save()
            else:
                print(form.errors)
        else:
            form = forms.ChangeData(instance=request.user)
        return render(request, 'userprofile.html', {'forms': form})
    else:
        return redirect('sign_up')


def pass_change(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return redirect('user_profile')
        else:
            form = PasswordChangeForm(user=request.user)
        return render(request, 'password.html', {'form': form})
    else:
        return redirect('login')
