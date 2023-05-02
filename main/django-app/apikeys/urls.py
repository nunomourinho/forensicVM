from django.urls import path
from .views import ProtectedView, RunScriptView

urlpatterns = [
    path('test/', ProtectedView.as_view(), name='test'),
    path('run-script/', RunScriptView.as_view(), name='run_script'),
]

