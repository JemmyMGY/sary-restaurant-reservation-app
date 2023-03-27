from django.urls import path, include
from rest_framework import routers

from .views import TablesViewSet


router = routers.DefaultRouter()
router.register(r'model-viewset', TablesViewSet) # newly registered ViewSet

urlpatterns = [
    path('tables-list', TablesViewSet.as_view({'get':'list'})),
    path('add-table', TablesViewSet.as_view({'post':'create'})),
    path('delete-table', TablesViewSet.as_view({'delete':'destroy'})),
    path('', include(router.urls)),
]