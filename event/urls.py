from django.urls import path
from . import views
urlpatterns = [
    path('signup/', views.signup, name='sign_up'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('user-profile/', views.profile, name='user_profile'),
    path('pass-change/', views.pass_change, name='pass_change'),
    path('my-event/', views.my_event, name='my_event'),
    path('event/<int:event_id>/book/', views.book_event, name='book_event'),
    path('my-booked-events/', views.booked_events, name='booked_events'),
    path('event/create/', views.event_create, name='event_create'),
    path('event/<int:event_id>/update/',
         views.event_update, name='event_update'),
    path('event/<int:event_id>/delete/',
         views.event_delete, name='event_delete'),
    path('admin/event/<int:event_id>/delete/',
         views.event_admin_delete, name='event_admin_delete'),
    path('bookings/<int:booking_id>/delete/',
         views.delete_booking, name='delete_booking'),
]
