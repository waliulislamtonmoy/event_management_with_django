# models.py
from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    CATEGORY_CHOICES = [
        ('conference', 'Conference'),
        ('concert', 'Concert'),
        ('workshop', 'Workshop'),
    ]
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateTimeField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    capacity = models.PositiveIntegerField()
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="events")

    def __str__(self):
        return self.name


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} booked {self.event.name}"
