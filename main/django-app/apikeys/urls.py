"""
The purpose of the program is to provide a set of API endpoints for managing a forensic virtual machine (VM).
Each view class represents a specific functionality that can be accessed through the corresponding API endpoint.
Here's a summary of each view's purpose:

ProtectedView: A view that requires API key authentication. Returns an access granted message if the API key is valid.

RunScriptView: Executes a script provided in the request data. Expects an API key and a script parameter.
Returns the script output and error code.

DeleteVMView: Deletes the forensic VM with the given UUID.

MountFolderView: Mounts a specified folder to the VM with the given UUID.

ResetVMView: Resets the forensic VM with the given UUID.

ShutdownVMView: Shuts down the forensic VM with the given UUID.

DownloadScreenshotsView: Downloads a zip file containing screenshots of the VM with the given UUID.

CreateSshKeysView: Adds a public SSH key to the authorized keys file of the forensic investigator user.

ForensicImageVMStatus: Retrieves the status of the forensic VM with the given UUID.

StartVMView: Starts the forensic VM with the given UUID.

StopVMView: Stops the forensic VM with the given UUID.

CheckVMExistsView: Checks if the forensic VM with the given UUID exists.

ScreenshotVMView: Takes a screenshot of the forensic VM with the given UUID.

MemorySnapshotView: Takes a memory snapshot of the forensic VM with the given UUID.

DownloadEvidenceView: Downloads the evidence file of the forensic VM with the given UUID.

CreateFoldersView: Creates necessary folders for the forensic VM.

ListISOFilesView: Lists ISO files available for the forensic VM.

UploadISOView: Uploads an ISO file for the forensic VM.

DeleteISOFileView: Deletes the specified ISO file for the forensic VM.

EjectCDROMView: Ejects the CD/DVD drive of the forensic VM with the given UUID.

InsertCDROMView: Inserts a specified CD/DVD into the forensic VM with the given UUID.

InsertNetworkCardView: Inserts a network card into the forensic VM with the given UUID.

ListPluginsView: Lists available plugins.

RunPluginView: Runs a specified plugin.

RecreateFoldersView: Recreates necessary folders for the forensic VM.

SnapshotListView: Lists snapshots for the forensic VM with the given UUID.

CreateSnapshotView: Creates a snapshot of the forensic VM with the given UUID.

RollbackSnapshotView: Rolls back to a specified snapshot of the forensic VM with the given UUID.

DeleteSnapshotView: Deletes the specified snapshot of the forensic VM with the given UUID.

MemorySizeView: Retrieves the memory size of the forensic VM with the given UUID.

ChangeMemorySizeView: Changes the memory size of the forensic VM with the given UUID.

GetAvailableMemoryView: Retrieves the available memory of the forensic VM.

StartTapInterfaceView: Starts the tap interface for capturing network traffic.

StopTapInterfaceView: Stops the tap interface for capturing network traffic.

CheckTapInterfaceView: Checks the status of the tap interface for capturing network traffic.

DownloadNetworkPcapView: Downloads a network pcap file for the forensic VM with the given UUID.

ChangeVMDateTimeView: Changes the date and time of the forensic VM with the given UUID.

RemoveVMDateTimeView: Removes the date and time configuration of the forensic VM with the given UUID.

DownloadVideoView: Downloads a video recording of the forensic VM with the given UUID.

RecordVideoVMView: Starts recording a video of the forensic VM with the given UUID.

StopVideoRecordingVMView: Stops recording a video of the forensic VM with the given UUID.

CheckRecordingStatusVMView: Checks the recording status of the forensic VM with the given UUID.

ListVideosView: Lists available video recordings of the forensic VM with the given UUID.

CheckUserAuthenticatedView: Checks if the user is authenticated via an API key.

"""
from django.views.generic import View
from django.urls import path
from .views import ProtectedView, RunScriptView, DeleteVMView, MountFolderView, ResetVMView, ShutdownVMView
from .views import DownloadScreenshotsView
from .views import CreateSshKeysView, ForensicImageVMStatus, StartVMView, StopVMView, CheckVMExistsView
from .views import ScreenshotVMView, MemorySnapshotView
from .views import DownloadEvidenceView, CreateFoldersView, ListISOFilesView, UploadISOView, DeleteISOFileView
from .views import EjectCDROMView, InsertCDROMView, InsertNetworkCardView, ListPluginsView, RunPluginView
from .views import RecreateFoldersView, SnapshotListView, CreateSnapshotView, RollbackSnapshotView, RollbackGoldenSnapshotView, DeleteSnapshotView
from .views import MemorySizeView, ChangeMemorySizeView, GetAvailableMemoryView, StartTapInterfaceView, StopTapInterfaceView
from .views import DownloadNetworkPcapView,CheckTapInterfaceView
from .views import ChangeVMDateTimeView, RemoveVMDateTimeView, DownloadVideoView
from .views import RecordVideoVMView, StopVideoRecordingVMView, CheckRecordingStatusVMView, ListVideosView
from .views import CheckUserAuthenticatedView, GenerateChainOfCustodyView, RecordCommentView
from .views import VirtualIntrospectionView, InsertMetrics, ExportVMDataToExcel, GenerateMetrics


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
    path('rollback-golden-snapshot/<uuid>/', RollbackGoldenSnapshotView.as_view(), name='rollback-golden-snapshot'),
    path('delete-snapshot/<uuid:uuid>/', DeleteSnapshotView.as_view(), name='delete-snapshot'),
    path('get-memory-size/<uuid>/', MemorySizeView.as_view(), name='get-memory-size'),
    path('change-memory-size/<uuid>/', ChangeMemorySizeView.as_view(), name='change_memory_size'),
    path('get-available-memory/', GetAvailableMemoryView.as_view(), name='get_available_memory'),
    path('start_tap/', StartTapInterfaceView.as_view(), name='start_tap'),
    path('stop_tap/', StopTapInterfaceView.as_view(), name='stop_tap'),
    path('check_tap/', CheckTapInterfaceView.as_view(), name='check_tap'),
    path('download_pcap/<str:uuid>/', DownloadNetworkPcapView.as_view(), name='download_pcap'),
    path('change_vm_datetime/', ChangeVMDateTimeView.as_view(), name='change_vm_datetime'),
    path('remove_vm_datetime/', RemoveVMDateTimeView.as_view(), name='remove_vm_datetime'),
    path('record_video/<str:uuid>/', RecordVideoVMView.as_view(), name='record_video'),
    path('stop_video/<str:uuid>/', StopVideoRecordingVMView.as_view(), name='stop_video'),
    path('check_recording/<str:uuid>/', CheckRecordingStatusVMView.as_view(), name='check_recording'),
    path('list_videos/<str:uuid>/', ListVideosView.as_view(), name='list_videos'),
    path('download_video/<uuid:uuid>/<str:filename>/', DownloadVideoView.as_view(), name='download_video'),
    path('check-authenticated/', CheckUserAuthenticatedView.as_view(), name='check-authenticated'),
    path('custody/<uuid>/', GenerateChainOfCustodyView.as_view(), name='generate-chain-off-custody'),
    path('record_comment/', RecordCommentView.as_view(), name='record_comment'),
    path('introspect/<uuid:uuid>/', VirtualIntrospectionView.as_view(), name='introspect_vm'),
    path('insertmetrics/<uuid>/', InsertMetrics.as_view(), name='insert_metrics'),
    path('exportmetrics/', ExportVMDataToExcel.as_view(), name='export_excel'),
    path('generatemetrics/', GenerateMetrics.as_view(), name='generate_metrics'),
]

