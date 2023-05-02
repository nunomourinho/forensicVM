from django.urls import path
from .views import ProtectedView

urlpatterns = [
    path('test/', ProtectedView.as_view(), name='test'),
]

