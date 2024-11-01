
from django.shortcuts import render
from django.contrib import messages
from event.models import Event, Booking
from django.db.models import Q
import calendar
import re


def home(request):
    events = Event.objects.all()
    booked_events = []
    query = request.GET.get('search', '').strip()
    category = request.GET.get('category', '')

    if request.user.is_authenticated:
        booked_events = Booking.objects.filter(
            user=request.user).values_list('event_id', flat=True)

    if query:
        filters = Q(name__icontains=query) | Q(location__icontains=query)

        date_pattern = re.search(
            r'(\d{1,2})\s+([a-zA-Z]+)|([a-zA-Z]+)\s+(\d{1,2})', query)
        if date_pattern:
            day = int(date_pattern.group(1) or date_pattern.group(4))
            month_str = (date_pattern.group(
                2) or date_pattern.group(3)).capitalize()
            month_number = {name: index for index, name in enumerate(
                calendar.month_abbr) if name}.get(month_str[:3])

            if month_number and 1 <= day <= 31:
                filters |= Q(date__month=month_number, date__day=day)
        else:
            month_number = {name: index for index, name in enumerate(
                calendar.month_abbr) if name}.get(query[:3].capitalize())
            if month_number:
                filters |= Q(date__month=month_number)

            if query.isdigit() and len(query) == 4:
                filters |= Q(date__year=int(query))

            if query.isdigit() and 1 <= int(query) <= 31:
                filters |= Q(date__day=int(query))

        events = events.filter(filters)

    if category:
        events = events.filter(category=category)

    return render(request, 'home.html', {
        'events': events,
        'booked_events': booked_events,
        'search_query': query,
        'selected_category': category,
    })
