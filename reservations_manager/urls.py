from django.urls import path, include
from rest_framework import routers

from .views import ReservationViewSet


router = routers.DefaultRouter()
router.register(r'model-viewset', ReservationViewSet) # newly registered ViewSet

urlpatterns = [
    path('reservations-list', ReservationViewSet.as_view({'get':'list'})),
    path('add-reservation', ReservationViewSet.as_view({'post':'create'})),
    path('delete-reservation', ReservationViewSet.as_view({'delete':'destroy'})),
    path('todays-reservations', ReservationViewSet.as_view({'get':'get_todays_reservations'})),
    path('available-slots', ReservationViewSet.as_view({'get':'get_available_slots'})),
    path('', include(router.urls)),
]