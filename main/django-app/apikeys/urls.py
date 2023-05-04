from django.urls import path
from .views import ProtectedView, RunScriptView
from .views import CreateSshKeysView, ForensicImageVMStatus

urlpatterns = [
    path('test/', ProtectedView.as_view(), name='test'),
    path('run-script/', RunScriptView.as_view(), name='run_script'),
    path('create-ssh-keys/', CreateSshKeysView.as_view(), name='create-ssh-keys'),
    path('forensic-image-vm-status/<str:uuid>/', ForensicImageView.as_view(), name='forensic-image-vm-status'),
]

