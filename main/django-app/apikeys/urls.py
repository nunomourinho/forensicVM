from django.views.generic import View
from django.urls import path
from .views import ProtectedView, RunScriptView, DeleteVMView, MountFolderView, ResetVMView, ShutdownVMView
from .views import DownloadScreenshotsView
from .views import CreateSshKeysView, ForensicImageVMStatus, StartVMView, StopVMView, CheckVMExistsView
from .views import ScreenshotVMView, MemorySnapshotView
from .views import DownloadEvidenceView, CreateFoldersView, ListISOFilesView, UploadISOView, DeleteISOFileView
from .views import EjectCDROMView, InsertCDROMView, InsertNetworkCardView, ListPluginsView, RunPluginView
from .views import RecreateFoldersView, SnapshotListView, CreateSnapshotView, RollbackSnapshotView, DeleteSnapshotView
from .views import MemorySizeView, ChangeMemorySizeView, GetAvailableMemoryView, StartTapInterfaceView, StopTapInterfaceView
from .views import CheckTapInterfaceView

urlpatterns = [
    #path('run-script/', RunScriptView.as_view(), name='run_script'),
    path('test/', ProtectedView.as_view(), name='test'),
    path('create-ssh-keys/', CreateSshKeysView.as_view(), name='create-ssh-keys'),
    path('forensic-image-vm-status/<str:uuid>/', ForensicImageVMStatus.as_view(), name='forensic-image-vm-status'),
    path('start-vm/<str:uuid>/', StartVMView.as_view(), name='start-vm'),
    path('stop-vm/<str:uuid>/', StopVMView.as_view(), name='stop-vm'),
    path('check-vm-exists/<uuid>/', CheckVMExistsView.as_view(), name='check-vm-exists'),
    path('delete-vm/<uuid>/', DeleteVMView.as_view(), name='delete-vm'),
    path('mount-folder/<uuid>/', MountFolderView.as_view(), name='mount-folder'),
    path('reset-vm/<uuid>/', ResetVMView.as_view(), name='reset-vm'),
    path('shutdown-vm/<uuid>/', ShutdownVMView.as_view(), name='shutdown_vm'),
    path('screenshot-vm/<str:uuid>/', ScreenshotVMView.as_view(), name='screenshot_vm'),
    path('download-screenshots/<str:uuid>/', DownloadScreenshotsView.as_view(), name='download_screenshots'),
    path('download-memory-dump/<uuid>/', MemorySnapshotView.as_view(), name='download_memory_dump'),
    path('download-evidence/<uuid>/', DownloadEvidenceView.as_view(), name='download_evidence'),
    path('create-folders/', CreateFoldersView.as_view(), name='create_folders'),
    path('list-iso-files/', ListISOFilesView.as_view(), name='list_iso_files'),
    path('upload-iso/', UploadISOView.as_view(), name='upload_iso'),
    path('delete-iso/<str:filename>/', DeleteISOFileView.as_view(), name='delete_iso'),
    path('eject-cdrom/<str:uuid>/', EjectCDROMView.as_view(), name='eject_cdrom'),
    path('insert-cdrom/<uuid>/<filename>/', InsertCDROMView.as_view(), name='insert-cdrom'),
    path('insert-network-card/<str:uuid>/', InsertNetworkCardView.as_view(), name='insert_network_card'),
    path('list-plugins/', ListPluginsView.as_view(), name='list-plugins'),
    path('run-plugin/', RunPluginView.as_view(), name='run-plugin'),
    path('api/recreate-folders/', RecreateFoldersView.as_view(), name='recreate-folders'),
    path('recreate-folders/', RecreateFoldersView.as_view(), name='recreate-folders'),
    path('snapshots-list/<uuid>/', SnapshotListView.as_view(), name='snapshot-list'),
    path('create-snapshot/<uuid>/', CreateSnapshotView.as_view(), name='create-snapshot'),
    path('rollback-snapshot/<uuid>/', RollbackSnapshotView.as_view(), name='rollback-snapshot'),
    path('delete-snapshot/<uuid:uuid>/', DeleteSnapshotView.as_view(), name='delete-snapshot'),
    path('get-memory-size/<uuid>/', MemorySizeView.as_view(), name='get-memory-size'),
    path('change-memory-size/<uuid>/', ChangeMemorySizeView.as_view(), name='change_memory_size'),
    path('get-available-memory/', GetAvailableMemoryView.as_view(), name='get_available_memory'),
    path('start_tap/', StartTapInterfaceView.as_view(), name='start_tap'),
    path('stop_tap/', StopTapInterfaceView.as_view(), name='stop_tap'),
    path('check_tap/', CheckTapInterfaceView.as_view(), name='check_tap'),
]

