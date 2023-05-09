from django.urls import path
from .views import ProtectedView, RunScriptView, DeleteVMView, MountFolderView, ResetVMView, ShutdownVMView
from .views import CreateSshKeysView, ForensicImageVMStatus, StartVMView, StopVMView, CheckVMExistsView

urlpatterns = [
    path('test/', ProtectedView.as_view(), name='test'),
    path('run-script/', RunScriptView.as_view(), name='run_script'),
    path('create-ssh-keys/', CreateSshKeysView.as_view(), name='create-ssh-keys'),
    path('forensic-image-vm-status/<str:uuid>/', ForensicImageVMStatus.as_view(), name='forensic-image-vm-status'),
    path('start-vm/<str:uuid>/', StartVMView.as_view(), name='start-vm'),
    path('stop-vm/<str:uuid>/', StopVMView.as_view(), name='stop-vm'),
    path('check-vm-exists/<uuid>/', CheckVMExistsView.as_view(), name='check-vm-exists'),
    path('delete-vm/<uuid>/', DeleteVMView.as_view(), name='delete-vm'),
    path('mount-folder/<uuid>/', MountFolderView.as_view(), name='mount-folder'),
    path('reset-vm/<uuid>/', ResetVMView.as_view(), name='reset-vm'),
    path('shutdown-vm/<uuid>/', ShutdownVMView.as_view(), name='shutdown_vm'),
]

