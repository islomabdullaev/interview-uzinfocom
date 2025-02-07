from django.urls import path
from booking.views import (
    PlaygroundBookingDeleteView, PlaygroundBookingDetailView,
    PlaygroundBookingView, PlaygroundView, PlaygroundDetailView)

urlpatterns = [
    path('playgrounds/', PlaygroundView.as_view()),
    path('playgrounds/detail/<uuid:id>', PlaygroundDetailView.as_view()),
    path('playgrounds/booking/', PlaygroundBookingView.as_view()),
    path('playgrounds/booking/detail/<str:id>', PlaygroundBookingDetailView.as_view()),
    path('playgrounds/booking/delete/<str:id>', PlaygroundBookingDeleteView.as_view()),
]