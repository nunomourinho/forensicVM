===============
apikeys package
===============

.. container:: wy-grid-for-nav

   .. container:: wy-side-scroll

      .. container:: wy-side-nav-search

         `ForensicVM <index.html>`__

         .. container::

      .. container:: wy-menu wy-menu-vertical

         .. container:: local-toc

            -  `apikeys package <#>`__

               -  `Subpackages <#subpackages>`__
               -  `Submodules <#submodules>`__
               -  `apikeys.admin module <#module-apikeys.admin>`__

                  -  ```ApiKeyAdmin`` <#apikeys.admin.ApiKeyAdmin>`__

                     -  ```ApiKeyAdmin.form`` <#apikeys.admin.ApiKeyAdmin.form>`__
                     -  ```ApiKeyAdmin.get_queryset()`` <#apikeys.admin.ApiKeyAdmin.get_queryset>`__
                     -  ```ApiKeyAdmin.list_display`` <#apikeys.admin.ApiKeyAdmin.list_display>`__
                     -  ```ApiKeyAdmin.masked_key()`` <#apikeys.admin.ApiKeyAdmin.masked_key>`__
                     -  ```ApiKeyAdmin.media`` <#apikeys.admin.ApiKeyAdmin.media>`__
                     -  ```ApiKeyAdmin.save_model()`` <#apikeys.admin.ApiKeyAdmin.save_model>`__

                  -  ```ApiKeyForm`` <#apikeys.admin.ApiKeyForm>`__

                     -  ```ApiKeyForm.Meta`` <#apikeys.admin.ApiKeyForm.Meta>`__

                        -  ```ApiKeyForm.Meta.exclude`` <#apikeys.admin.ApiKeyForm.Meta.exclude>`__
                        -  ```ApiKeyForm.Meta.fields`` <#apikeys.admin.ApiKeyForm.Meta.fields>`__
                        -  ```ApiKeyForm.Meta.model`` <#apikeys.admin.ApiKeyForm.Meta.model>`__

                     -  ```ApiKeyForm.base_fields`` <#apikeys.admin.ApiKeyForm.base_fields>`__
                     -  ```ApiKeyForm.declared_fields`` <#apikeys.admin.ApiKeyForm.declared_fields>`__
                     -  ```ApiKeyForm.media`` <#apikeys.admin.ApiKeyForm.media>`__

                  -  ```MaskedInput`` <#apikeys.admin.MaskedInput>`__

                     -  ```MaskedInput.format_value()`` <#apikeys.admin.MaskedInput.format_value>`__
                     -  ```MaskedInput.media`` <#apikeys.admin.MaskedInput.media>`__

               -  `apikeys.apps module <#module-apikeys.apps>`__

                  -  ```ApikeysConfig`` <#apikeys.apps.ApikeysConfig>`__

                     -  ```ApikeysConfig.default_auto_field`` <#apikeys.apps.ApikeysConfig.default_auto_field>`__
                     -  ```ApikeysConfig.name`` <#apikeys.apps.ApikeysConfig.name>`__

               -  `apikeys.models module <#module-apikeys.models>`__

                  -  ```ApiKey`` <#apikeys.models.ApiKey>`__

                     -  ```ApiKey.DoesNotExist`` <#apikeys.models.ApiKey.DoesNotExist>`__
                     -  ```ApiKey.MultipleObjectsReturned`` <#apikeys.models.ApiKey.MultipleObjectsReturned>`__
                     -  ```ApiKey.created_at`` <#apikeys.models.ApiKey.created_at>`__
                     -  ```ApiKey.get_next_by_created_at()`` <#apikeys.models.ApiKey.get_next_by_created_at>`__
                     -  ```ApiKey.get_previous_by_created_at()`` <#apikeys.models.ApiKey.get_previous_by_created_at>`__
                     -  ```ApiKey.id`` <#apikeys.models.ApiKey.id>`__
                     -  ```ApiKey.key`` <#apikeys.models.ApiKey.key>`__
                     -  ```ApiKey.mask_key()`` <#apikeys.models.ApiKey.mask_key>`__
                     -  ```ApiKey.objects`` <#apikeys.models.ApiKey.objects>`__
                     -  ```ApiKey.user`` <#apikeys.models.ApiKey.user>`__
                     -  ```ApiKey.user_id`` <#apikeys.models.ApiKey.user_id>`__

               -  `apikeys.serializers
                  module <#module-apikeys.serializers>`__

                  -  ```ApiKeySerializer`` <#apikeys.serializers.ApiKeySerializer>`__

                     -  ```ApiKeySerializer.Meta`` <#apikeys.serializers.ApiKeySerializer.Meta>`__

                        -  ```ApiKeySerializer.Meta.fields`` <#apikeys.serializers.ApiKeySerializer.Meta.fields>`__
                        -  ```ApiKeySerializer.Meta.model`` <#apikeys.serializers.ApiKeySerializer.Meta.model>`__

               -  `apikeys.tests module <#module-apikeys.tests>`__
               -  `apikeys.urls module <#module-apikeys.urls>`__
               -  `apikeys.views module <#module-apikeys.views>`__

                  -  ```ChangeMemorySizeView`` <#apikeys.views.ChangeMemorySizeView>`__

                     -  ```ChangeMemorySizeView.dispatch()`` <#apikeys.views.ChangeMemorySizeView.dispatch>`__
                     -  ```ChangeMemorySizeView.post()`` <#apikeys.views.ChangeMemorySizeView.post>`__

                  -  ```ChangeVMDateTimeView`` <#apikeys.views.ChangeVMDateTimeView>`__

                     -  ```ChangeVMDateTimeView.authentication_classes`` <#apikeys.views.ChangeVMDateTimeView.authentication_classes>`__
                     -  ```ChangeVMDateTimeView.dispatch()`` <#apikeys.views.ChangeVMDateTimeView.dispatch>`__
                     -  ```ChangeVMDateTimeView.permission_classes`` <#apikeys.views.ChangeVMDateTimeView.permission_classes>`__
                     -  ```ChangeVMDateTimeView.post()`` <#apikeys.views.ChangeVMDateTimeView.post>`__

                  -  ```CheckRecordingStatusVMView`` <#apikeys.views.CheckRecordingStatusVMView>`__

                     -  ```CheckRecordingStatusVMView.authentication_classes`` <#apikeys.views.CheckRecordingStatusVMView.authentication_classes>`__
                     -  ```CheckRecordingStatusVMView.dispatch()`` <#apikeys.views.CheckRecordingStatusVMView.dispatch>`__
                     -  ```CheckRecordingStatusVMView.get()`` <#apikeys.views.CheckRecordingStatusVMView.get>`__
                     -  ```CheckRecordingStatusVMView.get_user_or_key_error()`` <#apikeys.views.CheckRecordingStatusVMView.get_user_or_key_error>`__
                     -  ```CheckRecordingStatusVMView.permission_classes`` <#apikeys.views.CheckRecordingStatusVMView.permission_classes>`__

                  -  ```CheckTapInterfaceView`` <#apikeys.views.CheckTapInterfaceView>`__

                     -  ```CheckTapInterfaceView.authentication_classes`` <#apikeys.views.CheckTapInterfaceView.authentication_classes>`__
                     -  ```CheckTapInterfaceView.dispatch()`` <#apikeys.views.CheckTapInterfaceView.dispatch>`__
                     -  ```CheckTapInterfaceView.permission_classes`` <#apikeys.views.CheckTapInterfaceView.permission_classes>`__
                     -  ```CheckTapInterfaceView.post()`` <#apikeys.views.CheckTapInterfaceView.post>`__

                  -  ```CheckUserAuthenticatedView`` <#apikeys.views.CheckUserAuthenticatedView>`__

                     -  ```CheckUserAuthenticatedView.authentication_classes`` <#apikeys.views.CheckUserAuthenticatedView.authentication_classes>`__
                     -  ```CheckUserAuthenticatedView.get()`` <#apikeys.views.CheckUserAuthenticatedView.get>`__
                     -  ```CheckUserAuthenticatedView.get_user_or_key_error()`` <#apikeys.views.CheckUserAuthenticatedView.get_user_or_key_error>`__
                     -  ```CheckUserAuthenticatedView.permission_classes`` <#apikeys.views.CheckUserAuthenticatedView.permission_classes>`__

                  -  ```CheckVMExistsView`` <#apikeys.views.CheckVMExistsView>`__

                     -  ```CheckVMExistsView.authentication_classes`` <#apikeys.views.CheckVMExistsView.authentication_classes>`__
                     -  ```CheckVMExistsView.get()`` <#apikeys.views.CheckVMExistsView.get>`__
                     -  ```CheckVMExistsView.permission_classes`` <#apikeys.views.CheckVMExistsView.permission_classes>`__

                  -  ```CreateFoldersView`` <#apikeys.views.CreateFoldersView>`__

                     -  ```CreateFoldersView.authentication_classes`` <#apikeys.views.CreateFoldersView.authentication_classes>`__
                     -  ```CreateFoldersView.dispatch()`` <#apikeys.views.CreateFoldersView.dispatch>`__
                     -  ```CreateFoldersView.permission_classes`` <#apikeys.views.CreateFoldersView.permission_classes>`__
                     -  ```CreateFoldersView.post()`` <#apikeys.views.CreateFoldersView.post>`__

                  -  ```CreateSnapshotView`` <#apikeys.views.CreateSnapshotView>`__

                     -  ```CreateSnapshotView.dispatch()`` <#apikeys.views.CreateSnapshotView.dispatch>`__
                     -  ```CreateSnapshotView.post()`` <#apikeys.views.CreateSnapshotView.post>`__

                  -  ```CreateSshKeysView`` <#apikeys.views.CreateSshKeysView>`__

                     -  ```CreateSshKeysView.authentication_classes`` <#apikeys.views.CreateSshKeysView.authentication_classes>`__
                     -  ```CreateSshKeysView.permission_classes`` <#apikeys.views.CreateSshKeysView.permission_classes>`__
                     -  ```CreateSshKeysView.post()`` <#apikeys.views.CreateSshKeysView.post>`__

                  -  ```DeleteISOFileView`` <#apikeys.views.DeleteISOFileView>`__

                     -  ```DeleteISOFileView.authentication_classes`` <#apikeys.views.DeleteISOFileView.authentication_classes>`__
                     -  ```DeleteISOFileView.dispatch()`` <#apikeys.views.DeleteISOFileView.dispatch>`__
                     -  ```DeleteISOFileView.permission_classes`` <#apikeys.views.DeleteISOFileView.permission_classes>`__
                     -  ```DeleteISOFileView.post()`` <#apikeys.views.DeleteISOFileView.post>`__

                  -  ```DeleteSnapshotView`` <#apikeys.views.DeleteSnapshotView>`__

                     -  ```DeleteSnapshotView.dispatch()`` <#apikeys.views.DeleteSnapshotView.dispatch>`__
                     -  ```DeleteSnapshotView.post()`` <#apikeys.views.DeleteSnapshotView.post>`__

                  -  ```DeleteVMView`` <#apikeys.views.DeleteVMView>`__

                     -  ```DeleteVMView.authentication_classes`` <#apikeys.views.DeleteVMView.authentication_classes>`__
                     -  ```DeleteVMView.permission_classes`` <#apikeys.views.DeleteVMView.permission_classes>`__
                     -  ```DeleteVMView.post()`` <#apikeys.views.DeleteVMView.post>`__

                  -  ```DownloadEvidenceView`` <#apikeys.views.DownloadEvidenceView>`__

                     -  ```DownloadEvidenceView.authentication_classes`` <#apikeys.views.DownloadEvidenceView.authentication_classes>`__
                     -  ```DownloadEvidenceView.dispatch()`` <#apikeys.views.DownloadEvidenceView.dispatch>`__
                     -  ```DownloadEvidenceView.get()`` <#apikeys.views.DownloadEvidenceView.get>`__
                     -  ```DownloadEvidenceView.permission_classes`` <#apikeys.views.DownloadEvidenceView.permission_classes>`__

                  -  ```DownloadNetworkPcapView`` <#apikeys.views.DownloadNetworkPcapView>`__

                     -  ```DownloadNetworkPcapView.authentication_classes`` <#apikeys.views.DownloadNetworkPcapView.authentication_classes>`__
                     -  ```DownloadNetworkPcapView.dispatch()`` <#apikeys.views.DownloadNetworkPcapView.dispatch>`__
                     -  ```DownloadNetworkPcapView.get()`` <#apikeys.views.DownloadNetworkPcapView.get>`__
                     -  ```DownloadNetworkPcapView.permission_classes`` <#apikeys.views.DownloadNetworkPcapView.permission_classes>`__

                  -  ```DownloadScreenshotsView`` <#apikeys.views.DownloadScreenshotsView>`__

                     -  ```DownloadScreenshotsView.authentication_classes`` <#apikeys.views.DownloadScreenshotsView.authentication_classes>`__
                     -  ```DownloadScreenshotsView.dispatch()`` <#apikeys.views.DownloadScreenshotsView.dispatch>`__
                     -  ```DownloadScreenshotsView.get()`` <#apikeys.views.DownloadScreenshotsView.get>`__
                     -  ```DownloadScreenshotsView.permission_classes`` <#apikeys.views.DownloadScreenshotsView.permission_classes>`__

                  -  ```DownloadVideoView`` <#apikeys.views.DownloadVideoView>`__

                     -  ```DownloadVideoView.authentication_classes`` <#apikeys.views.DownloadVideoView.authentication_classes>`__
                     -  ```DownloadVideoView.get()`` <#apikeys.views.DownloadVideoView.get>`__
                     -  ```DownloadVideoView.get_user_or_key_error()`` <#apikeys.views.DownloadVideoView.get_user_or_key_error>`__
                     -  ```DownloadVideoView.permission_classes`` <#apikeys.views.DownloadVideoView.permission_classes>`__

                  -  ```EjectCDROMView`` <#apikeys.views.EjectCDROMView>`__

                     -  ```EjectCDROMView.authentication_classes`` <#apikeys.views.EjectCDROMView.authentication_classes>`__
                     -  ```EjectCDROMView.dispatch()`` <#apikeys.views.EjectCDROMView.dispatch>`__
                     -  ```EjectCDROMView.get()`` <#apikeys.views.EjectCDROMView.get>`__
                     -  ```EjectCDROMView.get_user_or_key_error()`` <#apikeys.views.EjectCDROMView.get_user_or_key_error>`__
                     -  ```EjectCDROMView.permission_classes`` <#apikeys.views.EjectCDROMView.permission_classes>`__

                  -  ```ForensicImageVMStatus`` <#apikeys.views.ForensicImageVMStatus>`__

                     -  ```ForensicImageVMStatus.authentication_classes`` <#apikeys.views.ForensicImageVMStatus.authentication_classes>`__
                     -  ```ForensicImageVMStatus.get()`` <#apikeys.views.ForensicImageVMStatus.get>`__
                     -  ```ForensicImageVMStatus.permission_classes`` <#apikeys.views.ForensicImageVMStatus.permission_classes>`__

                  -  ```GetAvailableMemoryView`` <#apikeys.views.GetAvailableMemoryView>`__

                     -  ```GetAvailableMemoryView.dispatch()`` <#apikeys.views.GetAvailableMemoryView.dispatch>`__
                     -  ```GetAvailableMemoryView.get()`` <#apikeys.views.GetAvailableMemoryView.get>`__

                  -  ```InsertCDROMView`` <#apikeys.views.InsertCDROMView>`__

                     -  ```InsertCDROMView.authentication_classes`` <#apikeys.views.InsertCDROMView.authentication_classes>`__
                     -  ```InsertCDROMView.dispatch()`` <#apikeys.views.InsertCDROMView.dispatch>`__
                     -  ```InsertCDROMView.get()`` <#apikeys.views.InsertCDROMView.get>`__
                     -  ```InsertCDROMView.get_user_or_key_error()`` <#apikeys.views.InsertCDROMView.get_user_or_key_error>`__
                     -  ```InsertCDROMView.permission_classes`` <#apikeys.views.InsertCDROMView.permission_classes>`__

                  -  ```InsertNetworkCardView`` <#apikeys.views.InsertNetworkCardView>`__

                     -  ```InsertNetworkCardView.authentication_classes`` <#apikeys.views.InsertNetworkCardView.authentication_classes>`__
                     -  ```InsertNetworkCardView.dispatch()`` <#apikeys.views.InsertNetworkCardView.dispatch>`__
                     -  ```InsertNetworkCardView.get()`` <#apikeys.views.InsertNetworkCardView.get>`__
                     -  ```InsertNetworkCardView.permission_classes`` <#apikeys.views.InsertNetworkCardView.permission_classes>`__

                  -  ```ListISOFilesView`` <#apikeys.views.ListISOFilesView>`__

                     -  ```ListISOFilesView.authentication_classes`` <#apikeys.views.ListISOFilesView.authentication_classes>`__
                     -  ```ListISOFilesView.get()`` <#apikeys.views.ListISOFilesView.get>`__
                     -  ```ListISOFilesView.permission_classes`` <#apikeys.views.ListISOFilesView.permission_classes>`__

                  -  ```ListPluginsView`` <#apikeys.views.ListPluginsView>`__

                     -  ```ListPluginsView.authentication_classes`` <#apikeys.views.ListPluginsView.authentication_classes>`__
                     -  ```ListPluginsView.get()`` <#apikeys.views.ListPluginsView.get>`__
                     -  ```ListPluginsView.permission_classes`` <#apikeys.views.ListPluginsView.permission_classes>`__

                  -  ```ListVideosView`` <#apikeys.views.ListVideosView>`__

                     -  ```ListVideosView.authentication_classes`` <#apikeys.views.ListVideosView.authentication_classes>`__
                     -  ```ListVideosView.get()`` <#apikeys.views.ListVideosView.get>`__
                     -  ```ListVideosView.get_user_or_key_error()`` <#apikeys.views.ListVideosView.get_user_or_key_error>`__
                     -  ```ListVideosView.permission_classes`` <#apikeys.views.ListVideosView.permission_classes>`__

                  -  ```MemorySizeView`` <#apikeys.views.MemorySizeView>`__

                     -  ```MemorySizeView.get()`` <#apikeys.views.MemorySizeView.get>`__

                  -  ```MemorySnapshotView`` <#apikeys.views.MemorySnapshotView>`__

                     -  ```MemorySnapshotView.authentication_classes`` <#apikeys.views.MemorySnapshotView.authentication_classes>`__
                     -  ```MemorySnapshotView.dispatch()`` <#apikeys.views.MemorySnapshotView.dispatch>`__
                     -  ```MemorySnapshotView.get()`` <#apikeys.views.MemorySnapshotView.get>`__
                     -  ```MemorySnapshotView.permission_classes`` <#apikeys.views.MemorySnapshotView.permission_classes>`__

                  -  ```MountFolderView`` <#apikeys.views.MountFolderView>`__

                     -  ```MountFolderView.authentication_classes`` <#apikeys.views.MountFolderView.authentication_classes>`__
                     -  ```MountFolderView.permission_classes`` <#apikeys.views.MountFolderView.permission_classes>`__
                     -  ```MountFolderView.post()`` <#apikeys.views.MountFolderView.post>`__

                  -  ```ProtectedView`` <#apikeys.views.ProtectedView>`__

                     -  ```ProtectedView.authentication_classes`` <#apikeys.views.ProtectedView.authentication_classes>`__
                     -  ```ProtectedView.get()`` <#apikeys.views.ProtectedView.get>`__
                     -  ```ProtectedView.permission_classes`` <#apikeys.views.ProtectedView.permission_classes>`__

                  -  ```RecordVideoVMView`` <#apikeys.views.RecordVideoVMView>`__

                     -  ```RecordVideoVMView.authentication_classes`` <#apikeys.views.RecordVideoVMView.authentication_classes>`__
                     -  ```RecordVideoVMView.dispatch()`` <#apikeys.views.RecordVideoVMView.dispatch>`__
                     -  ```RecordVideoVMView.get_user_or_key_error()`` <#apikeys.views.RecordVideoVMView.get_user_or_key_error>`__
                     -  ```RecordVideoVMView.permission_classes`` <#apikeys.views.RecordVideoVMView.permission_classes>`__
                     -  ```RecordVideoVMView.post()`` <#apikeys.views.RecordVideoVMView.post>`__

                  -  ```RecreateFoldersView`` <#apikeys.views.RecreateFoldersView>`__

                     -  ```RecreateFoldersView.authentication_classes`` <#apikeys.views.RecreateFoldersView.authentication_classes>`__
                     -  ```RecreateFoldersView.dispatch()`` <#apikeys.views.RecreateFoldersView.dispatch>`__
                     -  ```RecreateFoldersView.permission_classes`` <#apikeys.views.RecreateFoldersView.permission_classes>`__
                     -  ```RecreateFoldersView.post()`` <#apikeys.views.RecreateFoldersView.post>`__

                  -  ```RemoveVMDateTimeView`` <#apikeys.views.RemoveVMDateTimeView>`__

                     -  ```RemoveVMDateTimeView.authentication_classes`` <#apikeys.views.RemoveVMDateTimeView.authentication_classes>`__
                     -  ```RemoveVMDateTimeView.dispatch()`` <#apikeys.views.RemoveVMDateTimeView.dispatch>`__
                     -  ```RemoveVMDateTimeView.permission_classes`` <#apikeys.views.RemoveVMDateTimeView.permission_classes>`__
                     -  ```RemoveVMDateTimeView.post()`` <#apikeys.views.RemoveVMDateTimeView.post>`__

                  -  ```ResetVMView`` <#apikeys.views.ResetVMView>`__

                     -  ```ResetVMView.authentication_classes`` <#apikeys.views.ResetVMView.authentication_classes>`__
                     -  ```ResetVMView.dispatch()`` <#apikeys.views.ResetVMView.dispatch>`__
                     -  ```ResetVMView.get_user_or_key_error()`` <#apikeys.views.ResetVMView.get_user_or_key_error>`__
                     -  ```ResetVMView.permission_classes`` <#apikeys.views.ResetVMView.permission_classes>`__
                     -  ```ResetVMView.post()`` <#apikeys.views.ResetVMView.post>`__

                  -  ```RollbackSnapshotView`` <#apikeys.views.RollbackSnapshotView>`__

                     -  ```RollbackSnapshotView.dispatch()`` <#apikeys.views.RollbackSnapshotView.dispatch>`__
                     -  ```RollbackSnapshotView.post()`` <#apikeys.views.RollbackSnapshotView.post>`__

                  -  ```RunPluginView`` <#apikeys.views.RunPluginView>`__

                     -  ```RunPluginView.authentication_classes`` <#apikeys.views.RunPluginView.authentication_classes>`__
                     -  ```RunPluginView.get()`` <#apikeys.views.RunPluginView.get>`__
                     -  ```RunPluginView.permission_classes`` <#apikeys.views.RunPluginView.permission_classes>`__

                  -  ```RunScriptView`` <#apikeys.views.RunScriptView>`__

                     -  ```RunScriptView.authentication_classes`` <#apikeys.views.RunScriptView.authentication_classes>`__
                     -  ```RunScriptView.permission_classes`` <#apikeys.views.RunScriptView.permission_classes>`__
                     -  ```RunScriptView.post()`` <#apikeys.views.RunScriptView.post>`__

                  -  ```ScreenshotVMView`` <#apikeys.views.ScreenshotVMView>`__

                     -  ```ScreenshotVMView.authentication_classes`` <#apikeys.views.ScreenshotVMView.authentication_classes>`__
                     -  ```ScreenshotVMView.dispatch()`` <#apikeys.views.ScreenshotVMView.dispatch>`__
                     -  ```ScreenshotVMView.get_user_or_key_error()`` <#apikeys.views.ScreenshotVMView.get_user_or_key_error>`__
                     -  ```ScreenshotVMView.permission_classes`` <#apikeys.views.ScreenshotVMView.permission_classes>`__
                     -  ```ScreenshotVMView.post()`` <#apikeys.views.ScreenshotVMView.post>`__

                  -  ```ShutdownVMView`` <#apikeys.views.ShutdownVMView>`__

                     -  ```ShutdownVMView.authentication_classes`` <#apikeys.views.ShutdownVMView.authentication_classes>`__
                     -  ```ShutdownVMView.dispatch()`` <#apikeys.views.ShutdownVMView.dispatch>`__
                     -  ```ShutdownVMView.get_user_or_key_error()`` <#apikeys.views.ShutdownVMView.get_user_or_key_error>`__
                     -  ```ShutdownVMView.permission_classes`` <#apikeys.views.ShutdownVMView.permission_classes>`__
                     -  ```ShutdownVMView.post()`` <#apikeys.views.ShutdownVMView.post>`__

                  -  ```SnapshotListView`` <#apikeys.views.SnapshotListView>`__

                     -  ```SnapshotListView.dispatch()`` <#apikeys.views.SnapshotListView.dispatch>`__
                     -  ```SnapshotListView.get()`` <#apikeys.views.SnapshotListView.get>`__

                  -  ```StartTapInterfaceView`` <#apikeys.views.StartTapInterfaceView>`__

                     -  ```StartTapInterfaceView.authentication_classes`` <#apikeys.views.StartTapInterfaceView.authentication_classes>`__
                     -  ```StartTapInterfaceView.dispatch()`` <#apikeys.views.StartTapInterfaceView.dispatch>`__
                     -  ```StartTapInterfaceView.permission_classes`` <#apikeys.views.StartTapInterfaceView.permission_classes>`__
                     -  ```StartTapInterfaceView.post()`` <#apikeys.views.StartTapInterfaceView.post>`__

                  -  ```StartVMView`` <#apikeys.views.StartVMView>`__

                     -  ```StartVMView.authentication_classes`` <#apikeys.views.StartVMView.authentication_classes>`__
                     -  ```StartVMView.permission_classes`` <#apikeys.views.StartVMView.permission_classes>`__
                     -  ```StartVMView.post()`` <#apikeys.views.StartVMView.post>`__

                  -  ```StopTapInterfaceView`` <#apikeys.views.StopTapInterfaceView>`__

                     -  ```StopTapInterfaceView.authentication_classes`` <#apikeys.views.StopTapInterfaceView.authentication_classes>`__
                     -  ```StopTapInterfaceView.dispatch()`` <#apikeys.views.StopTapInterfaceView.dispatch>`__
                     -  ```StopTapInterfaceView.permission_classes`` <#apikeys.views.StopTapInterfaceView.permission_classes>`__
                     -  ```StopTapInterfaceView.post()`` <#apikeys.views.StopTapInterfaceView.post>`__

                  -  ```StopVMView`` <#apikeys.views.StopVMView>`__

                     -  ```StopVMView.authentication_classes`` <#apikeys.views.StopVMView.authentication_classes>`__
                     -  ```StopVMView.permission_classes`` <#apikeys.views.StopVMView.permission_classes>`__
                     -  ```StopVMView.post()`` <#apikeys.views.StopVMView.post>`__

                  -  ```StopVideoRecordingVMView`` <#apikeys.views.StopVideoRecordingVMView>`__

                     -  ```StopVideoRecordingVMView.authentication_classes`` <#apikeys.views.StopVideoRecordingVMView.authentication_classes>`__
                     -  ```StopVideoRecordingVMView.dispatch()`` <#apikeys.views.StopVideoRecordingVMView.dispatch>`__
                     -  ```StopVideoRecordingVMView.get_user_or_key_error()`` <#apikeys.views.StopVideoRecordingVMView.get_user_or_key_error>`__
                     -  ```StopVideoRecordingVMView.permission_classes`` <#apikeys.views.StopVideoRecordingVMView.permission_classes>`__
                     -  ```StopVideoRecordingVMView.post()`` <#apikeys.views.StopVideoRecordingVMView.post>`__

                  -  ```UploadISOView`` <#apikeys.views.UploadISOView>`__

                     -  ```UploadISOView.authentication_classes`` <#apikeys.views.UploadISOView.authentication_classes>`__
                     -  ```UploadISOView.dispatch()`` <#apikeys.views.UploadISOView.dispatch>`__
                     -  ```UploadISOView.permission_classes`` <#apikeys.views.UploadISOView.permission_classes>`__
                     -  ```UploadISOView.post()`` <#apikeys.views.UploadISOView.post>`__

                  -  ```change_qcow2()`` <#apikeys.views.change_qcow2>`__
                  -  ```create_and_format_qcow2()`` <#apikeys.views.create_and_format_qcow2>`__
                  -  ```create_snapshot()`` <#apikeys.views.create_snapshot>`__
                  -  ```create_video()`` <#apikeys.views.create_video>`__
                  -  ```delete_snapshot()`` <#apikeys.views.delete_snapshot>`__
                  -  ```eject_cdrom()`` <#apikeys.views.eject_cdrom>`__
                  -  ```find_available_port()`` <#apikeys.views.find_available_port>`__
                  -  ```generate_random_mac_address()`` <#apikeys.views.generate_random_mac_address>`__
                  -  ```get_available_memory()`` <#apikeys.views.get_available_memory>`__
                  -  ```get_plugin_info()`` <#apikeys.views.get_plugin_info>`__
                  -  ```get_snapshots()`` <#apikeys.views.get_snapshots>`__
                  -  ```insert_cdrom()`` <#apikeys.views.insert_cdrom>`__
                  -  ```insert_network_card()`` <#apikeys.views.insert_network_card>`__
                  -  ```memory_snapshot()`` <#apikeys.views.memory_snapshot>`__
                  -  ```rollback_snapshot()`` <#apikeys.views.rollback_snapshot>`__
                  -  ```screendump()`` <#apikeys.views.screendump>`__
                  -  ```system_reset()`` <#apikeys.views.system_reset>`__
                  -  ```system_shutdown()`` <#apikeys.views.system_shutdown>`__
                  -  ```validate_date()`` <#apikeys.views.validate_date>`__

               -  `Module contents <#module-apikeys>`__

   .. container:: section wy-nav-content-wrap

      `ForensicVM <index.html>`__

      .. container:: wy-nav-content

         .. container:: rst-content

            .. container::

               -  ` <index.html>`__
               -  apikeys package
               -  `View page source <_sources/apikeys.rst.txt>`__

               --------------

            .. container:: document

               .. container::

                  .. container:: section
                     :name: apikeys-package

                     .. rubric:: apikeys package
                        :name: apikeys-package

                     .. container:: section
                        :name: subpackages

                        .. rubric:: Subpackages
                           :name: subpackages

                        .. container:: toctree-wrapper compound

                           -  `apikeys.migrations
                              package <apikeys.migrations.html>`__

                              -  `Submodules <apikeys.migrations.html#submodules>`__
                              -  `apikeys.migrations.0001_initial
                                 module <apikeys.migrations.html#module-apikeys.migrations.0001_initial>`__

                                 -  ```Migration`` <apikeys.migrations.html#apikeys.migrations.0001_initial.Migration>`__

                                    -  ```Migration.dependencies`` <apikeys.migrations.html#apikeys.migrations.0001_initial.Migration.dependencies>`__
                                    -  ```Migration.initial`` <apikeys.migrations.html#apikeys.migrations.0001_initial.Migration.initial>`__
                                    -  ```Migration.operations`` <apikeys.migrations.html#apikeys.migrations.0001_initial.Migration.operations>`__

                              -  `apikeys.migrations.0002_alter_apikey_key
                                 module <apikeys.migrations.html#module-apikeys.migrations.0002_alter_apikey_key>`__

                                 -  ```Migration`` <apikeys.migrations.html#apikeys.migrations.0002_alter_apikey_key.Migration>`__

                                    -  ```Migration.dependencies`` <apikeys.migrations.html#apikeys.migrations.0002_alter_apikey_key.Migration.dependencies>`__
                                    -  ```Migration.operations`` <apikeys.migrations.html#apikeys.migrations.0002_alter_apikey_key.Migration.operations>`__

                              -  `apikeys.migrations.0003_alter_apikey_key
                                 module <apikeys.migrations.html#module-apikeys.migrations.0003_alter_apikey_key>`__

                                 -  ```Migration`` <apikeys.migrations.html#apikeys.migrations.0003_alter_apikey_key.Migration>`__

                                    -  ```Migration.dependencies`` <apikeys.migrations.html#apikeys.migrations.0003_alter_apikey_key.Migration.dependencies>`__
                                    -  ```Migration.operations`` <apikeys.migrations.html#apikeys.migrations.0003_alter_apikey_key.Migration.operations>`__

                              -  `apikeys.migrations.0004_alter_apikey_key
                                 module <apikeys.migrations.html#module-apikeys.migrations.0004_alter_apikey_key>`__

                                 -  ```Migration`` <apikeys.migrations.html#apikeys.migrations.0004_alter_apikey_key.Migration>`__

                                    -  ```Migration.dependencies`` <apikeys.migrations.html#apikeys.migrations.0004_alter_apikey_key.Migration.dependencies>`__
                                    -  ```Migration.operations`` <apikeys.migrations.html#apikeys.migrations.0004_alter_apikey_key.Migration.operations>`__

                              -  `Module
                                 contents <apikeys.migrations.html#module-apikeys.migrations>`__

                     .. container:: section
                        :name: submodules

                        .. rubric:: Submodules
                           :name: submodules

                     .. container:: section
                        :name: module-apikeys.admin

                        .. rubric:: apikeys.admin module
                           :name: apikeys.admin-module

                        *class*\ ``apikeys.admin.``\ ``ApiKeyAdmin``\ (\ *model*, *admin_site*\ )\ `[source] <_modules/apikeys/admin.html#ApiKeyAdmin>`__
                           Bases: ``ModelAdmin``

                           ModelAdmin for the ApiKey model.

                           This ModelAdmin provides customizations for
                           the admin interface for the ApiKey model. It
                           specifies the form to use, the list display
                           fields, and additional methods.

                           ``form``
                              alias of
                              ```ApiKeyForm`` <#apikeys.admin.ApiKeyForm>`__

                           ``get_queryset``\ (\ *request*\ )\ `[source] <_modules/apikeys/admin.html#ApiKeyAdmin.get_queryset>`__
                              Returns the queryset of ApiKey objects.

                              This method is used to filter the queryset
                              of ApiKey objects based on the user’s
                              privileges. If the user is a superuser,
                              all objects are returned. Otherwise, only
                              the objects belonging to the user are
                              returned.

                           ``list_display``\ *=('masked_key', 'created_at')*

                           ``masked_key``\ (\ *obj*\ )\ `[source] <_modules/apikeys/admin.html#ApiKeyAdmin.masked_key>`__
                              Returns the masked version of the API key.

                              This method takes an ApiKey object and
                              returns a masked version of the API key.
                              The masked version replaces most
                              characters with a mask character, except
                              for the last few characters which are
                              displayed as is.

                           *property*\ ``media``

                           ``save_model``\ (\ *request*, *obj*, *form*, *change*\ )\ `[source] <_modules/apikeys/admin.html#ApiKeyAdmin.save_model>`__
                              Saves the ApiKey object.

                              This method is called when saving an
                              ApiKey object through the admin interface.
                              It sets the user attribute of the object
                              to the current user and then saves the
                              object. Additionally, it displays a
                              success message with the generated API
                              key.

                        *class*\ ``apikeys.admin.``\ ``ApiKeyForm``\ (\ *data=None*, *files=None*, *auto_id='id_%s'*, *prefix=None*, *initial=None*, *error_class=<class 'django.forms.utils.ErrorList'>*, *label_suffix=None*, *empty_permitted=False*, *instance=None*, *use_required_attribute=None*, *renderer=None*\ )\ `[source] <_modules/apikeys/admin.html#ApiKeyForm>`__
                           Bases: ``ModelForm``

                           A form for the ApiKey model.

                           This form specifies the model, fields, and
                           any exclusions for the ApiKey model. It also
                           defines a custom widget for the ‘key’ field
                           to display a masked input.

                           *class*\ ``Meta``\ `[source] <_modules/apikeys/admin.html#ApiKeyForm.Meta>`__
                              Bases: ``object``

                              ``exclude``\ *=['key']*

                              ``fields``\ *=['user']*

                              ``model``
                                 alias of
                                 ```ApiKey`` <#apikeys.models.ApiKey>`__

                           ``base_fields``\ *={'user': <django.forms.models.ModelChoiceField object>}*

                           ``declared_fields``\ *={}*

                           *property*\ ``media``
                              Return all media required to render the
                              widgets on this form.

                        *class*\ ``apikeys.admin.``\ ``MaskedInput``\ (\ *attrs=None*, *mask_char='*'*, *mask_length=4*\ )\ `[source] <_modules/apikeys/admin.html#MaskedInput>`__
                           Bases: ``TextInput``

                           A custom form input widget that masks the
                           input value.

                           This widget replaces the actual value with a
                           masked version for display purposes. The
                           masked value consists of a configurable mask
                           character repeated for the length of the
                           value minus a specified mask length. The
                           remaining characters at the end of the value
                           are displayed as is.

                           ``format_value``\ (\ *value*\ )\ `[source] <_modules/apikeys/admin.html#MaskedInput.format_value>`__
                              Formats the input value with masking.

                              Args:
                                 value (str): The input value to be
                                 formatted.
                              Returns:
                                 str: The masked value.

                           *property*\ ``media``

                     .. container:: section
                        :name: module-apikeys.apps

                        .. rubric:: apikeys.apps module
                           :name: apikeys.apps-module

                        *class*\ ``apikeys.apps.``\ ``ApikeysConfig``\ (\ *app_name*, *app_module*\ )\ `[source] <_modules/apikeys/apps.html#ApikeysConfig>`__
                           Bases: ``AppConfig``

                           AppConfig for the ‘apikeys’ app.

                           This class represents the configuration for
                           the ‘apikeys’ app. It specifies the default
                           auto field and the name of the app.

                           ``default_auto_field``\ *='django.db.models.BigAutoField'*

                           ``name``\ *='apikeys'*

                     .. container:: section
                        :name: module-apikeys.models

                        .. rubric:: apikeys.models module
                           :name: apikeys.models-module

                        *class*\ ``apikeys.models.``\ ``ApiKey``\ (\ *\*args*, *\*\*kwargs*\ )\ `[source] <_modules/apikeys/models.html#ApiKey>`__
                           Bases: ``Model``

                           Model representing an API key associated with
                           a user.

                           *exception*\ ``DoesNotExist``
                              Bases: ``ObjectDoesNotExist``

                           *exception*\ ``MultipleObjectsReturned``
                              Bases: ``MultipleObjectsReturned``

                           ``created_at``
                              A wrapper for a deferred-loading field.
                              When the value is read from this object
                              the first time, the query is executed.

                           ``get_next_by_created_at``\ (\ *\**, *field=<django.db.models.fields.DateTimeField: created_at>*, *is_next=True*, *\**kwargs*\ )

                           ``get_previous_by_created_at``\ (\ *\**, *field=<django.db.models.fields.DateTimeField: created_at>*, *is_next=False*, *\**kwargs*\ )

                           ``id``
                              A wrapper for a deferred-loading field.
                              When the value is read from this object
                              the first time, the query is executed.

                           ``key``
                              A wrapper for a deferred-loading field.
                              When the value is read from this object
                              the first time, the query is executed.

                           ``mask_key``\ ()\ `[source] <_modules/apikeys/models.html#ApiKey.mask_key>`__
                              Return a masked version of the API key.

                           ``objects``\ *=<django.db.models.manager.Manager object>*

                           ``user``
                              Accessor to the related object on the
                              forward side of a many-to-one or
                              one-to-one (via ForwardOneToOneDescriptor
                              subclass) relation.

                              In the example:

                              .. container::
                              highlight-default notranslate

                                 .. container:: highlight

                                    ::

                                       class Child(Model):
                                           parent = ForeignKey(Parent, related_name='children')

                              ``Child.parent`` is a
                              ``ForwardManyToOneDescriptor`` instance.

                           ``user_id``

                     .. container:: section
                        :name: module-apikeys.serializers

                        .. rubric:: apikeys.serializers module
                           :name: apikeys.serializers-module

                        This code defines a serializer class
                        ApiKeySerializer that is used to serialize and
                        deserialize instances of the ApiKey model.

                        The ApiKeySerializer class inherits from the
                        ModelSerializer class provided by the Django
                        REST Framework. It specifies the ApiKey model as
                        the model attribute in the Meta class.

                        The fields attribute in the Meta class specifies
                        the fields that should be included in the
                        serialized representation of the ApiKey model.
                        In this case, it includes only the key field.

                        By using this serializer, one can easily convert
                        instances of the ApiKey model to JSON format
                        (serialization) and vice versa (deserialization)
                        when working with API requests and responses.

                        *class*\ ``apikeys.serializers.``\ ``ApiKeySerializer``\ (\ *\*args*, *\*\*kwargs*\ )\ `[source] <_modules/apikeys/serializers.html#ApiKeySerializer>`__
                           Bases: ``ModelSerializer``

                           *class*\ ``Meta``\ `[source] <_modules/apikeys/serializers.html#ApiKeySerializer.Meta>`__
                              Bases: ``object``

                              ``fields``\ *=['key']*

                              ``model``
                                 alias of
                                 ```ApiKey`` <#apikeys.models.ApiKey>`__

                     .. container:: section
                        :name: module-apikeys.tests

                        .. rubric:: apikeys.tests module
                           :name: apikeys.tests-module

                     .. container:: section
                        :name: module-apikeys.urls

                        .. rubric:: apikeys.urls module
                           :name: apikeys.urls-module

                        The purpose of the program is to provide a set
                        of API endpoints for managing a forensic virtual
                        machine (VM). Each view class represents a
                        specific functionality that can be accessed
                        through the corresponding API endpoint. Here’s a
                        summary of each view’s purpose:

                        ProtectedView: A view that requires API key
                        authentication. Returns an access granted
                        message if the API key is valid.

                        RunScriptView: Executes a script provided in the
                        request data. Expects an API key and a script
                        parameter. Returns the script output and error
                        code.

                        DeleteVMView: Deletes the forensic VM with the
                        given UUID.

                        MountFolderView: Mounts a specified folder to
                        the VM with the given UUID.

                        ResetVMView: Resets the forensic VM with the
                        given UUID.

                        ShutdownVMView: Shuts down the forensic VM with
                        the given UUID.

                        DownloadScreenshotsView: Downloads a zip file
                        containing screenshots of the VM with the given
                        UUID.

                        CreateSshKeysView: Adds a public SSH key to the
                        authorized keys file of the forensic
                        investigator user.

                        ForensicImageVMStatus: Retrieves the status of
                        the forensic VM with the given UUID.

                        StartVMView: Starts the forensic VM with the
                        given UUID.

                        StopVMView: Stops the forensic VM with the given
                        UUID.

                        CheckVMExistsView: Checks if the forensic VM
                        with the given UUID exists.

                        ScreenshotVMView: Takes a screenshot of the
                        forensic VM with the given UUID.

                        MemorySnapshotView: Takes a memory snapshot of
                        the forensic VM with the given UUID.

                        DownloadEvidenceView: Downloads the evidence
                        file of the forensic VM with the given UUID.

                        CreateFoldersView: Creates necessary folders for
                        the forensic VM.

                        ListISOFilesView: Lists ISO files available for
                        the forensic VM.

                        UploadISOView: Uploads an ISO file for the
                        forensic VM.

                        DeleteISOFileView: Deletes the specified ISO
                        file for the forensic VM.

                        EjectCDROMView: Ejects the CD/DVD drive of the
                        forensic VM with the given UUID.

                        InsertCDROMView: Inserts a specified CD/DVD into
                        the forensic VM with the given UUID.

                        InsertNetworkCardView: Inserts a network card
                        into the forensic VM with the given UUID.

                        ListPluginsView: Lists available plugins.

                        RunPluginView: Runs a specified plugin.

                        RecreateFoldersView: Recreates necessary folders
                        for the forensic VM.

                        SnapshotListView: Lists snapshots for the
                        forensic VM with the given UUID.

                        CreateSnapshotView: Creates a snapshot of the
                        forensic VM with the given UUID.

                        RollbackSnapshotView: Rolls back to a specified
                        snapshot of the forensic VM with the given UUID.

                        DeleteSnapshotView: Deletes the specified
                        snapshot of the forensic VM with the given UUID.

                        MemorySizeView: Retrieves the memory size of the
                        forensic VM with the given UUID.

                        ChangeMemorySizeView: Changes the memory size of
                        the forensic VM with the given UUID.

                        GetAvailableMemoryView: Retrieves the available
                        memory of the forensic VM.

                        StartTapInterfaceView: Starts the tap interface
                        for capturing network traffic.

                        StopTapInterfaceView: Stops the tap interface
                        for capturing network traffic.

                        CheckTapInterfaceView: Checks the status of the
                        tap interface for capturing network traffic.

                        DownloadNetworkPcapView: Downloads a network
                        pcap file for the forensic VM with the given
                        UUID.

                        ChangeVMDateTimeView: Changes the date and time
                        of the forensic VM with the given UUID.

                        RemoveVMDateTimeView: Removes the date and time
                        configuration of the forensic VM with the given
                        UUID.

                        DownloadVideoView: Downloads a video recording
                        of the forensic VM with the given UUID.

                        RecordVideoVMView: Starts recording a video of
                        the forensic VM with the given UUID.

                        StopVideoRecordingVMView: Stops recording a
                        video of the forensic VM with the given UUID.

                        CheckRecordingStatusVMView: Checks the recording
                        status of the forensic VM with the given UUID.

                        ListVideosView: Lists available video recordings
                        of the forensic VM with the given UUID.

                        CheckUserAuthenticatedView: Checks if the user
                        is authenticated via an API key.

                     .. container:: section
                        :name: module-apikeys.views

                        .. rubric:: apikeys.views module
                           :name: apikeys.views-module

                        *class*\ ``apikeys.views.``\ ``ChangeMemorySizeView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#ChangeMemorySizeView>`__
                           Bases: ``View``

                           API View that handles POST requests to change
                           the memory size of a Virtual Machine (VM).

                           This view requires an API key for
                           authentication and a POST body containing a
                           new memory size. If the API key is valid and
                           is associated with an active user, and the
                           POST body contains a valid memory size, the
                           script files in the VM directory are updated
                           with the new memory size.

                           If the API key is missing, invalid, or
                           associated with an inactive user, or if the
                           memory size is invalid, an error message is
                           returned.

                           The response indicates whether the memory
                           size update was successful or not in a JSON
                           format: {

                              .. container::

                                 “message”: <string>

                           }

                           ``dispatch``\ (\ *request*, *\*args*, *\*\*kwargs*\ )

                           ``post``\ (\ *request*, *uuid*\ )\ `[source] <_modules/apikeys/views.html#ChangeMemorySizeView.post>`__
                              Handles the POST request to change the
                              memory size of a VM.

                              Args:
                                 request: The HTTP request from the client. Expected to contain the API key in the headers and the new
                                    memory size in the POST body.

                                 uuid: The UUID of the VM whose memory
                                 size is to be changed.

                              Returns:
                                 JsonResponse: A JsonResponse that
                                 either contains a success message or an
                                 error message.

                        *class*\ ``apikeys.views.``\ ``ChangeVMDateTimeView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#ChangeVMDateTimeView>`__
                           Bases: ``View``

                           View to change the datetime in a VM’s
                           configuration.

                           The view has no authentication or permission
                           restrictions. The post method is used to
                           handle the updating of the datetime in the
                           configuration of a VM with a given UUID.

                           ``authentication_classes``\ *=[]*

                           ``dispatch``\ (\ *request*, *\*args*, *\*\*kwargs*\ )

                           ``permission_classes``\ *=[]*

                           *async*\ ``post``\ (\ *request*\ )\ `[source] <_modules/apikeys/views.html#ChangeVMDateTimeView.post>`__
                              Handle a POST request to change the
                              datetime in a VM’s configuration.

                              This method first checks if there is an
                              API key error. If there’s an API key
                              error, it returns a JSON response with the
                              error. The method then retrieves the UUID
                              and the datetime from the POST data and
                              validates the datetime format. If the
                              datetime format is invalid, it returns a
                              JSON response indicating the error. It
                              locates the .sh configuration file for the
                              VM with the provided UUID, reads its
                              content, and changes or adds a line with
                              the ‘-rtc base=’ string and the new
                              datetime. If successful, the method
                              returns a JSON response indicating the
                              successful operation. If there’s an error,
                              it returns a JSON response with the error
                              message.

                              .. container:: section
                                 :name: parameters

                                 .. rubric:: Parameters:
                                    :name: parameters

                                 requestdjango.http.HttpRequest
                                    The request instance for the current
                                    request.

                              .. container:: section
                                 :name: returns

                                 .. rubric:: Returns:
                                    :name: returns

                                 django.http.JsonResponse
                                    A JsonResponse indicating the result
                                    of the operation.

                        *class*\ ``apikeys.views.``\ ``CheckRecordingStatusVMView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#CheckRecordingStatusVMView>`__
                           Bases: ``View``

                           View to check the status of video recording.

                           The view uses session authentication and has
                           no permission restrictions. The get method is
                           used to handle the checking of the video
                           recording status for a VM with a given UUID.

                           ``authentication_classes``\ *=[<class 'rest_framework.authentication.SessionAuthentication'>]*

                           ``dispatch``\ (\ *request*, *\*args*, *\*\*kwargs*\ )

                           *async*\ ``get``\ (\ *request*, *uuid*\ )\ `[source] <_modules/apikeys/views.html#CheckRecordingStatusVMView.get>`__
                              Handle a GET request to check video
                              recording status for a VM with a given
                              UUID.

                              This method first checks if the user is
                              authenticated or if there is an API key
                              error. If there’s an API key error, it
                              returns a JSON response with the error. If
                              the UUID is present in the recordings and
                              is recording, it returns a JSON response
                              indicating the recording is in progress.
                              If the UUID is not present or not
                              recording, it returns a JSON response
                              indicating no recording is in progress.

                              .. container:: section
                                 :name: id1

                                 .. rubric:: Parameters:
                                    :name: parameters-1

                                 requestdjango.http.HttpRequest
                                    The request instance for the current
                                    request.
                                 uuidstr
                                    The UUID of the VM for which the
                                    recording status should be checked.

                              .. container:: section
                                 :name: id2

                                 .. rubric:: Returns:
                                    :name: returns-1

                                 django.http.JsonResponse
                                    A JsonResponse indicating the result
                                    of the operation.

                           ``get_user_or_key_error``\ (\ *request*\ )\ `[source] <_modules/apikeys/views.html#CheckRecordingStatusVMView.get_user_or_key_error>`__
                              Check if the user is authenticated or if
                              there is an API key error.

                              This method checks if the user associated
                              with the request is authenticated. If the
                              user is not authenticated, it checks if
                              there’s an API key in the request. If the
                              API key is valid and associated with an
                              active user, the method returns this user.
                              If the API key is not valid or the user is
                              not active, it returns a JSON response
                              with the corresponding error. If there’s
                              no API key at all, it returns a JSON
                              response indicating that the API key is
                              required.

                              .. container:: section
                                 :name: id3

                                 .. rubric:: Parameters:
                                    :name: parameters-2

                                 requestdjango.http.HttpRequest
                                    The request instance for the current
                                    request.

                              .. container:: section
                                 :name: id4

                                 .. rubric:: Returns:
                                    :name: returns-2

                                 tuple
                                    A tuple where the first element is
                                    the authenticated user or None, and
                                    the second element is a JsonResponse
                                    with an error message or None.

                           ``permission_classes``\ *=[]*

                        *class*\ ``apikeys.views.``\ ``CheckTapInterfaceView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#CheckTapInterfaceView>`__
                           Bases: ``View``

                           View to check the status of the tap interface
                           of a VM.

                           The view has no authentication or permission
                           restrictions. The post method is used to
                           handle the status checking of the tap
                           interface of a VM.

                           ``authentication_classes``\ *=[]*

                           ``dispatch``\ (\ *request*, *\*args*, *\*\*kwargs*\ )

                           ``permission_classes``\ *=[]*

                           *async*\ ``post``\ (\ *request*\ )\ `[source] <_modules/apikeys/views.html#CheckTapInterfaceView.post>`__
                              Handle a POST request to check the status
                              of the tap interface of a VM.

                              This method first checks if there is an
                              API key error. If there’s an API key
                              error, it returns a JSON response with the
                              error. The method then gets the UUID from
                              the POST data and checks the status of the
                              tap interface. It executes shell commands
                              to get the tap interface and checks its
                              status. If the tap interface is up, the
                              method returns a JSON response with a
                              positive status and message. If the tap
                              interface is down, the method returns a
                              JSON response with a negative status and
                              message.

                              .. container:: section
                                 :name: id5

                                 .. rubric:: Parameters:
                                    :name: parameters-3

                                 requestdjango.http.HttpRequest
                                    The request instance for the current
                                    request.

                              .. container:: section
                                 :name: id6

                                 .. rubric:: Returns:
                                    :name: returns-3

                                 django.http.JsonResponse
                                    A JsonResponse with the status and
                                    message about the status of the tap
                                    interface.

                        *class*\ ``apikeys.views.``\ ``CheckUserAuthenticatedView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#CheckUserAuthenticatedView>`__
                           Bases: ``View``

                           A Django View class for checking if a user is
                           authenticated.

                           This class uses SessionAuthentication for
                           user authentication. It doesn’t implement any
                           specific permission classes.

                           .. container:: section
                              :name: attributes

                              .. rubric:: Attributes:
                                 :name: attributes

                              authentication_classeslist
                                 List of authentication classes the view
                                 uses. Here, it’s SessionAuthentication.
                              permission_classeslist
                                 List of permission classes the view
                                 uses. Here, it’s an empty list.

                           .. container:: section
                              :name: methods

                              .. rubric:: Methods:
                                 :name: methods

                              get(request):
                                 Returns a JsonResponse indicating if a
                                 user is authenticated.

                              ``authentication_classes``\ *=[<class 'rest_framework.authentication.SessionAuthentication'>]*

                              ``get``\ (\ *request*\ )\ `[source] <_modules/apikeys/views.html#CheckUserAuthenticatedView.get>`__
                                 Handles GET request to the view.

                                 This method retrieves a user from the
                                 request or an API key error if one
                                 occurred. It then checks if the user is
                                 authenticated by checking if any API
                                 key error occurred. If the user is
                                 authenticated, it returns a JSON
                                 response with the ‘authenticated’ key
                                 set to True.

                                 .. container:: section
                                    :name: id7

                                    .. rubric:: Parameters:
                                       :name: parameters-4

                                    requestdjango.http.HttpRequest
                                       The request instance for the
                                       current request.

                                 .. container:: section
                                    :name: id8

                                    .. rubric:: Returns:
                                       :name: returns-4

                                    django.http.JsonResponse
                                       A JsonResponse that indicates if
                                       the user is authenticated.

                              ``get_user_or_key_error``\ (\ *request*\ )\ `[source] <_modules/apikeys/views.html#CheckUserAuthenticatedView.get_user_or_key_error>`__
                                 Retrieves the authenticated user from
                                 the request or returns an API key
                                 error.

                                 This method attempts to get an
                                 authenticated user from the request. If
                                 the user is authenticated, it will
                                 return the user and None for the error.
                                 If the user is not authenticated, it
                                 will attempt to authenticate the user
                                 using an API key provided in the
                                 request. If the API key is valid and
                                 associated with an active user, it
                                 returns the user and None for the
                                 error. If the API key is invalid or the
                                 user associated with the key is not
                                 active, it returns None for the user
                                 and a JsonResponse indicating the
                                 error. If no API key is provided in the
                                 request, it returns None for the user
                                 and a JsonResponse indicating that an
                                 API key is required.

                                 .. container:: section
                                    :name: id9

                                    .. rubric:: Parameters:
                                       :name: parameters-5

                                    requestdjango.http.HttpRequest
                                       The request instance for the
                                       current request.

                                 .. container:: section
                                    :name: id10

                                    .. rubric:: Returns:
                                       :name: returns-5

                                    tuple
                                       A tuple where the first element
                                       is the authenticated user or None
                                       if no user could be
                                       authenticated, and the second
                                       element is None or a JsonResponse
                                       containing an error message.

                              ``permission_classes``\ *=[]*

                        *class*\ ``apikeys.views.``\ ``CheckVMExistsView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#CheckVMExistsView>`__
                           Bases: ``APIView``

                           This Django View handles GET requests to
                           check if a VM exists. It authenticates the
                           request and then checks the existence of the
                           specified VM’s directory in the filesystem.

                           The VM is identified by its UUID, which
                           should be included in the URL of the request.

                           ``authentication_classes``\ *=[]*

                           ``get``\ (\ *request*, *uuid*\ )\ `[source] <_modules/apikeys/views.html#CheckVMExistsView.get>`__
                              This method handles the GET request to
                              check if a VM exists. It checks for user
                              authentication, verifies the existence of
                              the VM, and then returns a JSON response
                              with the result.

                              Args:
                                 request (django.http.HttpRequest): The
                                 request instance. uuid (str): The UUID
                                 of the VM to be checked.
                              Returns:
                                 rest_framework.response.Response: A
                                 JSON response indicating whether the VM
                                 exists.

                           ``permission_classes``\ *=[]*

                        *class*\ ``apikeys.views.``\ ``CreateFoldersView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#CreateFoldersView>`__
                           Bases: ``View``

                           This class-based view handles the POST
                           request to create specified folders in a
                           qcow2 disk image.

                           The method checks the validity and activity
                           status of the provided API key. If the API
                           key is invalid or belongs to an inactive
                           user, it returns an error message.

                           It then retrieves the list of folders and the
                           UUID path from the request data. It uses the
                           UUID path to form the path to the qcow2 file.

                           It checks if the qcow2 file exists. If it
                           doesn’t, it returns an error.

                           It calls the change_qcow2 function to create
                           the folders in the qcow2 file. If successful,
                           it returns a success message. If an error
                           occurs, it returns an error message.

                           Attributes: authentication_classes (list): A
                           list of authentication classes to use for the
                           view. permission_classes (list): A list of
                           permission classes to use for the view.

                           Methods: post(request): Asynchronously
                           handles the POST request.

                           ``authentication_classes``\ *=[]*

                           ``dispatch``\ (\ *request*, *\*args*, *\*\*kwargs*\ )

                           ``permission_classes``\ *=[]*

                           *async*\ ``post``\ (\ *request*\ )\ `[source] <_modules/apikeys/views.html#CreateFoldersView.post>`__
                              Asynchronously handles the POST request to
                              create folders in a qcow2 file.

                              Parameters: request (HttpRequest): The
                              request object that has triggered this
                              method.

                              Returns: JsonResponse: A JSON object
                              containing a success message if the
                              folders were created successfully,

                                 .. container::

                                    or an error message otherwise.

                        *class*\ ``apikeys.views.``\ ``CreateSnapshotView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#CreateSnapshotView>`__
                           Bases: ``View``

                           API View that handles POST requests to create
                           a snapshot of a specific VM.

                           This view requires an API key for
                           authentication. If the API key is valid and
                           is associated with an active user, it calls
                           the create_snapshot asynchronous function to
                           create the snapshot.

                           If the API key is missing, invalid, or
                           associated with an inactive user, an error
                           message is returned.

                           The response indicates either the snapshot
                           name or an error message in a JSON format: {

                              .. container::

                                 “snapshot_name”: <string>

                           } or {

                              .. container::

                                 “error”: <string>

                           }

                           ``dispatch``\ (\ *request*, *\*args*, *\*\*kwargs*\ )

                           *async*\ ``post``\ (\ *request*, *uuid*\ )\ `[source] <_modules/apikeys/views.html#CreateSnapshotView.post>`__
                              Handles the POST request to create a
                              snapshot of a VM.

                              Args:
                                 request: The HTTP request from the
                                 client. Expected to contain the API key
                                 in the headers. uuid: The UUID of the
                                 VM to create the snapshot.
                              Returns:
                                 JsonResponse: A JsonResponse that
                                 either contains the snapshot name or an
                                 error message.

                        *class*\ ``apikeys.views.``\ ``CreateSshKeysView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#CreateSshKeysView>`__
                           Bases: ``APIView``

                           API endpoint that allows the creation of SSH
                           keys by adding a public key to the authorized
                           keys file of the forensic investigator user.

                           This view accepts a POST request with a
                           public key as a parameter. The public key is
                           added to the authorized keys file of the
                           forensic investigator user. An API key or
                           session-based authentication is required.

                           ``authentication_classes``\ *=[]*

                           ``permission_classes``\ *=[]*

                           ``post``\ (\ *request*\ )\ `[source] <_modules/apikeys/views.html#CreateSshKeysView.post>`__
                              Adds a public key to the authorized keys
                              file of the forensic investigator user.

                              Args:
                                 request: The POST request received by
                                 the server.
                              Returns:
                                 Response: A Django Response object
                                 containing the result of adding the
                                 public key to the authorized keys file.

                        *class*\ ``apikeys.views.``\ ``DeleteISOFileView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#DeleteISOFileView>`__
                           Bases: ``View``

                           This is a Django view that provides an
                           endpoint for deleting an ISO file from a
                           specified directory.

                           The DeleteISOFileView class handles HTTP POST
                           requests to delete an ISO file identified by
                           its filename.

                           The class uses Django’s View, which means it
                           can handle different types of HTTP requests.
                           It currently only implements handling of POST
                           requests via the defined post() method.

                           Attributes:
                              authentication_classes (list): A list of
                              authentication classes the view should
                              use. It’s empty in this case.
                              permission_classes (list): A list of
                              permissions the view should enforce. It’s
                              empty in this case.

                           ``authentication_classes``\ *=[]*

                           ``dispatch``\ (\ *request*, *\*args*, *\*\*kwargs*\ )

                           ``permission_classes``\ *=[]*

                           ``post``\ (\ *request*, *filename*\ )\ `[source] <_modules/apikeys/views.html#DeleteISOFileView.post>`__
                              This method handles the POST request to
                              delete an ISO file.

                              It first validates the API key from the
                              request. If the API key is valid and
                              belongs to an active user, it checks if
                              the ISO directory and the specified ISO
                              file exist. If they do, it deletes the ISO
                              file and returns a confirmation message.

                              Parameters: request (HttpRequest): The
                              request object that has triggered this
                              method. filename (str): The name of the
                              ISO file to be deleted.

                              Returns: JsonResponse: A JSON object
                              containing a confirmation message or an
                              error message with an HTTP status code.

                        *class*\ ``apikeys.views.``\ ``DeleteSnapshotView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#DeleteSnapshotView>`__
                           Bases: ``View``

                           API View that handles POST requests to delete
                           a snapshot of a specific VM.

                           This view requires an API key for
                           authentication. If the API key is valid and
                           is associated with an active user, it calls
                           the delete_snapshot asynchronous function to
                           delete the snapshot.

                           If the API key is missing, invalid, or
                           associated with an inactive user, or if the
                           snapshot name is missing in the request data,
                           an error message is returned.

                           The response indicates either a success or an
                           error message in a JSON format: {

                              .. container::

                                 “message”: <string>

                           } or {

                              .. container::

                                 “error”: <string>

                           }

                           ``dispatch``\ (\ *request*, *\*args*, *\*\*kwargs*\ )

                           *async*\ ``post``\ (\ *request*, *uuid*\ )\ `[source] <_modules/apikeys/views.html#DeleteSnapshotView.post>`__
                              Handles the POST request to delete a
                              snapshot of a VM.

                              Args:
                                 request: The HTTP request from the client. Expected to contain the API key in the headers,
                                    and the snapshot name in the request
                                    data.

                                 uuid: The UUID of the VM whose snapshot
                                 is to be deleted.

                              Returns:
                                 JsonResponse: A JsonResponse that
                                 either contains a success message or an
                                 error message.

                        *class*\ ``apikeys.views.``\ ``DeleteVMView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#DeleteVMView>`__
                           Bases: ``APIView``

                           This Django View handles POST requests to
                           delete a VM. It authenticates the request and
                           then removes the specified VM’s directory
                           from the filesystem.

                           The VM is identified by its UUID, which
                           should be included in the URL of the request.

                           ``authentication_classes``\ *=[]*

                           ``permission_classes``\ *=[]*

                           ``post``\ (\ *request*, *uuid*\ )\ `[source] <_modules/apikeys/views.html#DeleteVMView.post>`__
                              This method handles the POST request to
                              delete a VM. It checks for user
                              authentication, verifies the existence of
                              the VM, and then deletes the VM’s
                              directory.

                              Args:
                                 request (django.http.HttpRequest): The
                                 request instance. uuid (str): The UUID
                                 of the VM to be deleted.
                              Returns:
                                 rest_framework.response.Response: A
                                 JSON response with the result of the
                                 operation.

                        *class*\ ``apikeys.views.``\ ``DownloadEvidenceView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#DownloadEvidenceView>`__
                           Bases: ``View``

                           This class-based view handles the GET request
                           to download a VMDK evidence file related to a
                           specific VM.

                           The method checks the validity and activity
                           status of the provided API key. If the API
                           key is invalid or belongs to an inactive
                           user, it returns an error message.

                           It uses the UUID from the URL parameters to
                           form the path to the VM directory and checks
                           if it exists.

                           It then forms the path to the qcow2 file and
                           converts it to a VMDK file using qemu-img. If
                           this process fails, it returns an error
                           message.

                           It checks if the VMDK evidence file exists.
                           If it doesn’t, it returns an error.

                           Finally, it returns the evidence file as a
                           FileResponse, allowing the client to download
                           it.

                           Attributes: authentication_classes (list): A
                           list of authentication classes to use for the
                           view. permission_classes (list): A list of
                           permission classes to use for the view.

                           Methods: get(request, uuid): Asynchronously
                           handles the GET request.

                           ``authentication_classes``\ *=[]*

                           ``dispatch``\ (\ *request*, *\*args*, *\*\*kwargs*\ )

                           *async*\ ``get``\ (\ *request*, *uuid*\ )\ `[source] <_modules/apikeys/views.html#DownloadEvidenceView.get>`__
                              Asynchronously handles the GET request to
                              download a VMDK evidence file.

                              Parameters: request (HttpRequest): The
                              request object that has triggered this
                              method. uuid (str): The UUID of the VM.

                              Returns: FileResponse: A FileResponse
                              object containing the VMDK evidence file,

                                 .. container::

                                    or a JsonResponse object containing
                                    an error message.

                           ``permission_classes``\ *=[]*

                        *class*\ ``apikeys.views.``\ ``DownloadNetworkPcapView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#DownloadNetworkPcapView>`__
                           Bases: ``View``

                           View to download the pcap files of a VM.

                           The view has no authentication or permission
                           restrictions. The get method is used to
                           handle the downloading of pcap files of a VM
                           with a given UUID.

                           ``authentication_classes``\ *=[]*

                           ``dispatch``\ (\ *request*, *\*args*, *\*\*kwargs*\ )

                           *async*\ ``get``\ (\ *request*, *uuid*\ )\ `[source] <_modules/apikeys/views.html#DownloadNetworkPcapView.get>`__
                              Handle a GET request to download the pcap
                              files of a VM.

                              This method first checks if there is an
                              API key error. If there’s an API key
                              error, it returns a JSON response with the
                              error. The method then checks if the VM
                              with the provided UUID exists. If the VM
                              does not exist, it returns a JSON response
                              indicating the error. It creates a zip
                              file of all pcap files associated with the
                              VM. If successful, the method returns a
                              FileResponse with the created zip file.

                              .. container:: section
                                 :name: id11

                                 .. rubric:: Parameters:
                                    :name: parameters-6

                                 requestdjango.http.HttpRequest
                                    The request instance for the current
                                    request.
                                 uuidstr
                                    The UUID of the VM.

                              .. container:: section
                                 :name: id12

                                 .. rubric:: Returns:
                                    :name: returns-6

                                 django.http.FileResponse
                                    A FileResponse with the zip file of
                                    the pcap files of the VM.

                           ``permission_classes``\ *=[]*

                        *class*\ ``apikeys.views.``\ ``DownloadScreenshotsView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#DownloadScreenshotsView>`__
                           Bases: ``View``

                           This is an API view for downloading all the
                           screenshots of a Virtual Machine (VM) as a
                           ZIP file. It requires the UUID of the VM to
                           be specified as a path parameter in the URL.

                           Authentication is done via an API key which
                           must be included in the request headers.

                           This view will attempt to collect all the
                           screenshots of the VM, convert them to JPG
                           format if necessary, compress them into a ZIP
                           file, and then return it as a file download.

                           ``authentication_classes``\ *=[]*

                           ``dispatch``\ (\ *request*, *\*args*, *\*\*kwargs*\ )

                           *async*\ ``get``\ (\ *request*, *uuid*\ )\ `[source] <_modules/apikeys/views.html#DownloadScreenshotsView.get>`__
                              Handle the GET request to the
                              DownloadScreenshotsView.

                              The function will first authenticate the
                              user using the API key provided in the
                              headers. If the user is authenticated, it
                              will proceed to collect all the
                              screenshots of the VM specified by the
                              UUID in the URL, convert them to JPG
                              format, compress them into a ZIP file, and
                              then return the ZIP file as a response.

                              Args:
                                 request: The HTTP request. uuid: The
                                 UUID of the VM to download the
                                 screenshots from.
                              Returns:
                                 A FileResponse with the ZIP file
                                 containing all screenshots. If an error
                                 occurs, a JsonResponse with an error
                                 message will be returned.

                           ``permission_classes``\ *=[]*

                        *class*\ ``apikeys.views.``\ ``DownloadVideoView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#DownloadVideoView>`__
                           Bases: ``APIView``

                           A Django APIView class for downloading a
                           video file.

                           This class uses SessionAuthentication for
                           user authentication. It doesn’t implement any
                           specific permission classes.

                           .. container:: section
                              :name: id13

                              .. rubric:: Attributes:
                                 :name: attributes-1

                              authentication_classeslist
                                 List of authentication classes the view
                                 uses. Here, it’s SessionAuthentication.
                              permission_classeslist
                                 List of permission classes the view
                                 uses. Here, it’s an empty list.

                           .. container:: section
                              :name: id14

                              .. rubric:: Methods:
                                 :name: methods-1

                              get(request, uuid, filename):
                                 Returns a FileResponse to download a
                                 video file.

                              ``authentication_classes``\ *=[<class 'rest_framework.authentication.SessionAuthentication'>]*

                              ``get``\ (\ *request*, *uuid*, *filename*\ )\ `[source] <_modules/apikeys/views.html#DownloadVideoView.get>`__
                                 Handles GET request to download a
                                 video.

                                 This method checks if the user is
                                 authenticated, validates the filename,
                                 constructs the file path, checks if the
                                 file exists, and returns a FileResponse
                                 for the client to download the video.

                                 .. container:: section
                                    :name: id15

                                    .. rubric:: Parameters:
                                       :name: parameters-7

                                    requestdjango.http.HttpRequest
                                       The request instance for the
                                       current request.
                                    uuidstr
                                       The unique identifier for the
                                       video file’s directory.
                                    filenamestr
                                       The name of the video file to
                                       download.

                                 .. container:: section
                                    :name: id16

                                    .. rubric:: Returns:
                                       :name: returns-7

                                    django.http.FileResponse
                                       A FileResponse that initiates the
                                       video file download.

                                 .. container:: section
                                    :name: raises

                                    .. rubric:: Raises:
                                       :name: raises

                                    Http404
                                       If the video file does not exist.

                              ``get_user_or_key_error``\ (\ *request*\ )\ `[source] <_modules/apikeys/views.html#DownloadVideoView.get_user_or_key_error>`__
                                 Retrieves the authenticated user from
                                 the request or returns an API key
                                 error.

                                 This method attempts to get an
                                 authenticated user from the request. If
                                 the user is authenticated, it will
                                 return the user and None for the error.
                                 If the user is not authenticated, it
                                 will attempt to authenticate the user
                                 using an API key provided in the
                                 request. If the API key is valid and
                                 associated with an active user, it
                                 returns the user and None for the
                                 error. If the API key is invalid or the
                                 user associated with the key is not
                                 active, it returns None for the user
                                 and a JsonResponse indicating the
                                 error. If no API key is provided in the
                                 request, it returns None for the user
                                 and a JsonResponse indicating that an
                                 API key is required.

                                 .. container:: section
                                    :name: id17

                                    .. rubric:: Parameters:
                                       :name: parameters-8

                                    requestdjango.http.HttpRequest
                                       The request instance for the
                                       current request.

                                 .. container:: section
                                    :name: id18

                                    .. rubric:: Returns:
                                       :name: returns-8

                                    tuple
                                       A tuple where the first element
                                       is the authenticated user or None
                                       if no user could be
                                       authenticated, and the second
                                       element is None or a JsonResponse
                                       containing an error message.

                              ``permission_classes``\ *=[]*

                        *class*\ ``apikeys.views.``\ ``EjectCDROMView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#EjectCDROMView>`__
                           Bases: ``View``

                           This is a Django view that provides an
                           endpoint for ejecting the CD-ROM from a
                           virtual machine.

                           The EjectCDROMView class handles HTTP GET
                           requests to eject the CD-ROM from a virtual
                           machine identified by its unique identifier
                           (uuid).

                           The class uses Django’s View, which means it
                           can handle different types of HTTP requests.
                           It currently only implements handling of GET
                           requests via the defined get() method. It
                           also supports authentication via sessions.

                           Attributes:
                              authentication_classes (list): A list of authentication classes the view should use.
                                 It includes SessionAuthentication.

                              permission_classes (list): A list of
                              permissions the view should enforce. Empty
                              in this case.

                           ``authentication_classes``\ *=[<class 'rest_framework.authentication.SessionAuthentication'>]*

                           ``dispatch``\ (\ *request*, *\*args*, *\*\*kwargs*\ )

                           *async*\ ``get``\ (\ *request*, *uuid*\ )\ `[source] <_modules/apikeys/views.html#EjectCDROMView.get>`__
                              This method handles the GET request to
                              eject the CD-ROM from a virtual machine.

                              It first validates the user or API key
                              from the request. If the user is
                              authenticated or the API key is valid, it
                              calls the asynchronous function
                              eject_cdrom() to eject the CD-ROM and
                              returns a confirmation message.

                              Parameters: request (HttpRequest): The
                              request object that has triggered this
                              method. uuid (str): The unique identifier
                              of the virtual machine.

                              Returns: JsonResponse: A JSON object
                              containing a confirmation message or an
                              error message with an HTTP status code.

                           ``get_user_or_key_error``\ (\ *request*\ )\ `[source] <_modules/apikeys/views.html#EjectCDROMView.get_user_or_key_error>`__
                              This method handles the user
                              authentication and API key validation.

                              It checks if the user is authenticated. If
                              not, it validates the API key from the
                              request. If the API key is invalid or
                              belongs to an inactive user, it returns a
                              JSON response with an error message.

                              Parameters: request (HttpRequest): The
                              request object that has triggered this
                              method.

                              Returns: tuple: A tuple containing the
                              user (if authenticated or API key is
                              valid) and a JSON response (if any error
                              occurs).

                           ``permission_classes``\ *=[]*

                        *class*\ ``apikeys.views.``\ ``ForensicImageVMStatus``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#ForensicImageVMStatus>`__
                           Bases: ``APIView``

                           API endpoint that allows retrieval of the
                           status of a forensic image VM via GET
                           requests.

                           This view accepts a GET request with a UUID
                           and returns the status of the corresponding
                           forensic image VM. If the VM path or mode
                           file cannot be found, it returns a 404 Not
                           Found error. An API key or session-based
                           authentication is required.

                           ``authentication_classes``\ *=[<class 'rest_framework.authentication.SessionAuthentication'>]*

                           ``get``\ (\ *request*, *uuid*\ )\ `[source] <_modules/apikeys/views.html#ForensicImageVMStatus.get>`__
                              Retrieves the status of the forensic image
                              VM specified by the UUID.

                              Args:
                                 request: The GET request received by
                                 the server. uuid: The UUID of the
                                 forensic image VM.
                              Returns:
                                 Response: A Django Response object
                                 containing the VM status and related
                                 information.

                           ``permission_classes``\ *=[]*

                        *class*\ ``apikeys.views.``\ ``GetAvailableMemoryView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#GetAvailableMemoryView>`__
                           Bases: ``View``

                           API View that handles GET requests to
                           retrieve available system memory.

                           This view requires an API key for
                           authentication. If the API key is valid and
                           is associated with an active user, the
                           system’s available memory is returned. The
                           available memory is calculated using the
                           get_available_memory function.

                           If the API key is missing, invalid, or
                           associated with an inactive user, an error
                           message is returned.

                           The available memory is returned in a JSON
                           format: {

                              .. container::

                                 “available_memory”: <float>

                           }

                           ``dispatch``\ (\ *request*, *\*args*, *\*\*kwargs*\ )

                           ``get``\ (\ *request*\ )\ `[source] <_modules/apikeys/views.html#GetAvailableMemoryView.get>`__
                              Handles the GET request to retrieve the
                              system’s available memory.

                              Args:
                                 request: The HTTP request from the
                                 client. Expected to contain the API key
                                 in the headers.
                              Returns:
                                 JsonResponse: A JsonResponse that
                                 either contains the available memory or
                                 an error message.

                        *class*\ ``apikeys.views.``\ ``InsertCDROMView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#InsertCDROMView>`__
                           Bases: ``View``

                           This is a Django view that provides an
                           endpoint for inserting a CD-ROM into a
                           virtual machine.

                           The InsertCDROMView class handles HTTP GET
                           requests to insert a CD-ROM into a virtual
                           machine identified by its unique identifier
                           (uuid) and the filename of the ISO image.

                           The class uses Django’s View, which means it
                           can handle different types of HTTP requests.
                           It currently only implements handling of GET
                           requests via the defined get() method. It
                           also supports authentication via sessions.

                           Attributes:
                              authentication_classes (list): A list of authentication classes the view should use.
                                 It includes SessionAuthentication.

                              permission_classes (list): A list of
                              permissions the view should enforce. Empty
                              in this case.

                           ``authentication_classes``\ *=[<class 'rest_framework.authentication.SessionAuthentication'>]*

                           ``dispatch``\ (\ *request*, *\*args*, *\*\*kwargs*\ )

                           *async*\ ``get``\ (\ *request*, *uuid*, *filename*\ )\ `[source] <_modules/apikeys/views.html#InsertCDROMView.get>`__
                              This method handles the GET request to
                              insert a CD-ROM into a virtual machine.

                              It first validates the user or API key
                              from the request. If the user is
                              authenticated or the API key is valid, it
                              calls the asynchronous function
                              insert_cdrom() to insert the CD-ROM and
                              returns a confirmation message.

                              Parameters: request (HttpRequest): The
                              request object that has triggered this
                              method. uuid (str): The unique identifier
                              of the virtual machine. filename (str):
                              The filename of the ISO image to insert
                              into the CD-ROM drive.

                              Returns: JsonResponse: A JSON object
                              containing a confirmation message or an
                              error message with an HTTP status code.

                           ``get_user_or_key_error``\ (\ *request*\ )\ `[source] <_modules/apikeys/views.html#InsertCDROMView.get_user_or_key_error>`__
                              This method handles the user
                              authentication and API key validation.

                              It checks if the user is authenticated. If
                              not, it validates the API key from the
                              request. If the API key is invalid or
                              belongs to an inactive user, it returns a
                              JSON response with an error message.

                              Parameters: request (HttpRequest): The
                              request object that has triggered this
                              method.

                              Returns: tuple: A tuple containing the
                              user (if authenticated or API key is
                              valid) and a JSON response (if any error
                              occurs).

                           ``permission_classes``\ *=[]*

                        *class*\ ``apikeys.views.``\ ``InsertNetworkCardView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#InsertNetworkCardView>`__
                           Bases: ``View``

                           This is a Django view that provides an
                           endpoint for inserting a network card into a
                           virtual machine.

                           The InsertNetworkCardView class handles HTTP
                           GET requests to insert a network card into a
                           virtual machine identified by its unique
                           identifier (uuid). The class uses Django’s
                           View, which means it can handle different
                           types of HTTP requests. It currently only
                           implements handling of GET requests via the
                           defined get() method.

                           Attributes:
                              authentication_classes (list): A list of
                              authentication classes the view should
                              use. Empty in this case.
                              permission_classes (list): A list of
                              permissions the view should enforce. Empty
                              in this case.

                           ``authentication_classes``\ *=[]*

                           ``dispatch``\ (\ *request*, *\*args*, *\*\*kwargs*\ )

                           *async*\ ``get``\ (\ *request*, *uuid*\ )\ `[source] <_modules/apikeys/views.html#InsertNetworkCardView.get>`__
                              This method handles the GET request to
                              insert a network card into a virtual
                              machine.

                              It first validates the API key from the
                              request. If the key is valid, it calls the
                              asynchronous function
                              insert_network_card() to insert the
                              network card and returns a confirmation
                              message.

                              Parameters: request (HttpRequest): The
                              request object that has triggered this
                              method. uuid (str): The unique identifier
                              of the virtual machine.

                              Returns: JsonResponse: A JSON object
                              containing a confirmation message or an
                              error message with an HTTP status code.

                           ``permission_classes``\ *=[]*

                        *class*\ ``apikeys.views.``\ ``ListISOFilesView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#ListISOFilesView>`__
                           Bases: ``APIView``

                           This is a Django view that provides an
                           endpoint for retrieving a list of all ISO
                           files in a specified directory.

                           The ListISOFilesView class handles HTTP GET
                           requests to retrieve the ISO files.

                           The class uses Django’s APIView, which allows
                           it to handle different types of HTTP
                           requests. It currently only implements
                           handling of GET requests via the defined
                           get() method.

                           Attributes:
                              authentication_classes (list): A list of
                              authentication classes the view should
                              use. It’s empty in this case.
                              permission_classes (list): A list of
                              permissions the view should enforce. It’s
                              empty in this case.

                           ``authentication_classes``\ *=[]*

                           ``get``\ (\ *request*\ )\ `[source] <_modules/apikeys/views.html#ListISOFilesView.get>`__
                              This method handles the GET request to
                              list all ISO files.

                              It first validates the API key from the
                              request. If the API key is valid and
                              belongs to an active user, it checks if
                              the ISO directory exists and retrieves a
                              list of all ISO files in the directory. If
                              the directory does not exist, it returns
                              an error message.

                              Parameters: request (HttpRequest): The
                              request object that has triggered this
                              method.

                              Returns: JsonResponse: A JSON object
                              containing a list of all ISO files in the
                              directory or an error message with an HTTP
                              status code.

                           ``permission_classes``\ *=[]*

                        *class*\ ``apikeys.views.``\ ``ListPluginsView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#ListPluginsView>`__
                           Bases: ``APIView``

                           This is a Django REST Framework view that
                           extends from the APIView base class.

                           The ListPluginsView class defines behavior
                           for handling HTTP GET requests on the URL
                           path associated with it. The purpose of this
                           class is to provide an endpoint that responds
                           with a list of available forensic plugins.
                           The view uses Django’s APIView, which means
                           it can handle different types of HTTP
                           requests. It currently only implements
                           handling of GET requests via the defined
                           get() method.

                           Attributes:
                              authentication_classes (list): A list of
                              authentication classes the view should
                              use. Empty in this case.
                              permission_classes (list): A list of
                              permissions the view should enforce. Empty
                              in this case.

                           ``authentication_classes``\ *=[]*

                           ``get``\ (\ *request*\ )\ `[source] <_modules/apikeys/views.html#ListPluginsView.get>`__
                              Handles GET requests to list all available
                              forensic plugins.

                              The method retrieves the API key from the
                              request headers and validates it. If the
                              API key is invalid or belongs to an
                              inactive user, an error response is
                              returned.

                              The method then reads the ‘plugins’
                              directory and looks for ‘run.sh’ files in
                              each of the subdirectories. For each such
                              file found, it gets the plugin information
                              by calling the get_plugin_info() function.

                              If the ‘plugins’ directory does not exist,
                              an error response is returned.

                              Parameters: request (HttpRequest): The
                              request object that has triggered this
                              method.

                              Returns: JsonResponse: A JSON object
                              containing a list of all available plugins
                              with their names, descriptions and
                              directories.

                           ``permission_classes``\ *=[]*

                        *class*\ ``apikeys.views.``\ ``ListVideosView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#ListVideosView>`__
                           Bases: ``APIView``

                           A Django APIView class for listing all the
                           .mp4 video files in a specific directory.

                           This class uses SessionAuthentication for
                           user authentication. It doesn’t implement any
                           specific permission classes.

                           .. container:: section
                              :name: id19

                              .. rubric:: Attributes:
                                 :name: attributes-2

                              authentication_classeslist
                                 List of authentication classes the view
                                 uses. Here, it’s SessionAuthentication.
                              permission_classeslist
                                 List of permission classes the view
                                 uses. Here, it’s an empty list.

                           .. container:: section
                              :name: id20

                              .. rubric:: Methods:
                                 :name: methods-2

                              get(request, uuid):
                                 Returns a JsonResponse with a list of
                                 all .mp4 video files in the specified
                                 directory.

                              ``authentication_classes``\ *=[<class 'rest_framework.authentication.SessionAuthentication'>]*

                              ``get``\ (\ *request*, *uuid*\ )\ `[source] <_modules/apikeys/views.html#ListVideosView.get>`__
                                 Handles GET request to list all .mp4
                                 video files in a specific directory.

                                 This method checks if the user is
                                 authenticated, constructs the video
                                 directory path, checks if the directory
                                 exists, and returns a JsonResponse
                                 containing a list of all .mp4 video
                                 files in the directory, sorted in
                                 ascending order.

                                 .. container:: section
                                    :name: id21

                                    .. rubric:: Parameters:
                                       :name: parameters-9

                                    requestdjango.http.HttpRequest
                                       The request instance for the
                                       current request.
                                    uuidstr
                                       The unique identifier for the
                                       video files’ directory.

                                 .. container:: section
                                    :name: id22

                                    .. rubric:: Returns:
                                       :name: returns-9

                                    django.http.JsonResponse
                                       A JsonResponse containing a list
                                       of all .mp4 video files in the
                                       specified directory.

                              ``get_user_or_key_error``\ (\ *request*\ )\ `[source] <_modules/apikeys/views.html#ListVideosView.get_user_or_key_error>`__
                                 Retrieves the authenticated user from
                                 the request or returns an API key
                                 error.

                                 This method attempts to get an
                                 authenticated user from the request. If
                                 the user is authenticated, it will
                                 return the user and None for the error.
                                 If the user is not authenticated, it
                                 will attempt to authenticate the user
                                 using an API key provided in the
                                 request. If the API key is valid and
                                 associated with an active user, it
                                 returns the user and None for the
                                 error. If the API key is invalid or the
                                 user associated with the key is not
                                 active, it returns None for the user
                                 and a JsonResponse indicating the
                                 error. If no API key is provided in the
                                 request, it returns None for the user
                                 and a JsonResponse indicating that an
                                 API key is required.

                                 .. container:: section
                                    :name: id23

                                    .. rubric:: Parameters:
                                       :name: parameters-10

                                    requestdjango.http.HttpRequest
                                       The request instance for the
                                       current request.

                                 .. container:: section
                                    :name: id24

                                    .. rubric:: Returns:
                                       :name: returns-10

                                    tuple
                                       A tuple where the first element
                                       is the authenticated user or None
                                       if no user could be
                                       authenticated, and the second
                                       element is None or a JsonResponse
                                       containing an error message.

                              ``permission_classes``\ *=[]*

                        *class*\ ``apikeys.views.``\ ``MemorySizeView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#MemorySizeView>`__
                           Bases: ``View``

                           API View that handles GET requests to fetch
                           the current memory size of a Virtual Machine
                           (VM).

                           This view requires an API key for
                           authentication. If the API key is valid and
                           is associated with an active user, the memory
                           size is retrieved from the script files in
                           the VM directory.

                           If the API key is missing, invalid, or
                           associated with an inactive user, or if the
                           memory size cannot be found, an error message
                           is returned.

                           The response indicates either the memory size
                           or an error message in a JSON format: {

                              .. container::

                                 “memory_size”: <int>

                           } or {

                              .. container::

                                 “error”: <string>

                           }

                           ``get``\ (\ *request*, *uuid*\ )\ `[source] <_modules/apikeys/views.html#MemorySizeView.get>`__
                              Handles the GET request to fetch the
                              memory size of a VM.

                              Args:
                                 request: The HTTP request from the
                                 client. Expected to contain the API key
                                 in the headers. uuid: The UUID of the
                                 VM whose memory size is to be fetched.
                              Returns:
                                 JsonResponse: A JsonResponse that
                                 either contains the memory size or an
                                 error message.

                        *class*\ ``apikeys.views.``\ ``MemorySnapshotView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#MemorySnapshotView>`__
                           Bases: ``View``

                           This is an API view for creating a memory
                           snapshot of a Virtual Machine (VM) and
                           downloading it. It requires the UUID of the
                           VM to be specified as a path parameter in the
                           URL.

                           Authentication is done via an API key which
                           must be included in the request headers.

                           This view will attempt to create a memory
                           snapshot of the VM and then return it as a
                           file download.

                           ``authentication_classes``\ *=[]*

                           ``dispatch``\ (\ *request*, *\*args*, *\*\*kwargs*\ )

                           *async*\ ``get``\ (\ *request*, *uuid*\ )\ `[source] <_modules/apikeys/views.html#MemorySnapshotView.get>`__
                              Handle the GET request to the
                              MemorySnapshotView.

                              The function will first authenticate the
                              user using the API key provided in the
                              headers. If the user is authenticated, it
                              will proceed to create a memory snapshot
                              of the VM specified by the UUID in the URL
                              and then return the snapshot file as a
                              response.

                              Args:
                                 request: The HTTP request. uuid: The
                                 UUID of the VM to create a memory
                                 snapshot of.
                              Returns:
                                 A FileResponse with the memory snapshot
                                 file. If an error occurs, a
                                 JsonResponse with an error message will
                                 be returned.

                           ``permission_classes``\ *=[]*

                        *class*\ ``apikeys.views.``\ ``MountFolderView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#MountFolderView>`__
                           Bases: ``APIView``

                           This Django View handles POST requests to
                           mount a folder in a VM. It authenticates the
                           request and then executes a mount command to
                           bind the specified folder to a location
                           within the VM’s filesystem.

                           The VM is identified by its UUID, which
                           should be included in the URL of the request.

                           The folder to be mounted should be specified
                           in the request’s JSON body using the ‘folder’
                           key.

                           ``authentication_classes``\ *=[]*

                           ``permission_classes``\ *=[]*

                           ``post``\ (\ *request*, *uuid*\ )\ `[source] <_modules/apikeys/views.html#MountFolderView.post>`__
                              This method handles the POST request to
                              mount a folder in a VM. It checks for user
                              authentication, verifies the input folder
                              path, and then sends the mount command.

                              Args:
                                 request (django.http.HttpRequest): The
                                 request instance. uuid (str): The UUID
                                 of the VM where the folder is to be
                                 mounted.
                              Returns:
                                 rest_framework.response.Response: A
                                 JSON response with the result of the
                                 operation.

                        *class*\ ``apikeys.views.``\ ``ProtectedView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#ProtectedView>`__
                           Bases: ``APIView``

                           API endpoint that creates a protected view
                           requiring an API key for access.

                           This view accepts a GET request and checks
                           for the presence of an API key in the request
                           headers. If a valid API key is found, the
                           access is granted and a success message is
                           returned. An API key is required for
                           accessing this view.

                           ``authentication_classes``\ *=[]*

                           ``get``\ (\ *request*\ )\ `[source] <_modules/apikeys/views.html#ProtectedView.get>`__
                              Handles the GET request and checks for the
                              presence of a valid API key.

                              Args:
                                 request: The GET request received by
                                 the server.
                              Returns:
                                 Response: A Django Response object
                                 indicating the result of the access
                                 check.

                           ``permission_classes``\ *=[]*

                        *class*\ ``apikeys.views.``\ ``RecordVideoVMView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#RecordVideoVMView>`__
                           Bases: ``View``

                           A Django View class that handles the video
                           recording process of a virtual machine.

                           This class implements the POST HTTP method to
                           start and manage the recording of a video. If
                           the requested virtual machine (identified by
                           uuid) exists and is not already recording, it
                           starts a new recording, creating a video file
                           in a specified directory. The recording runs
                           asynchronously for a maximum duration of
                           three hours or until it is manually stopped.

                           If the virtual machine is already recording,
                           the POST request will return an error.

                           ``authentication_classes``\ *=[<class 'rest_framework.authentication.SessionAuthentication'>]*

                           ``dispatch``\ (\ *request*, *\*args*, *\*\*kwargs*\ )

                           ``get_user_or_key_error``\ (\ *request*\ )\ `[source] <_modules/apikeys/views.html#RecordVideoVMView.get_user_or_key_error>`__
                              Check if the user is authenticated or if
                              there is an API key error.

                              This method checks if the user associated
                              with the request is authenticated. If the
                              user is not authenticated, it checks if
                              there’s an API key in the request. If the
                              API key is valid and associated with an
                              active user, the method returns this user.
                              If the API key is not valid or the user is
                              not active, it returns a JSON response
                              with the corresponding error. If there’s
                              no API key at all, it returns a JSON
                              response indicating that the API key is
                              required.

                              .. container:: section
                                 :name: id25

                                 .. rubric:: Parameters:
                                    :name: parameters-11

                                 requestdjango.http.HttpRequest
                                    The request instance for the current
                                    request.

                              .. container:: section
                                 :name: id26

                                 .. rubric:: Returns:
                                    :name: returns-11

                                 tuple
                                    A tuple where the first element is
                                    the authenticated user or None, and
                                    the second element is a JsonResponse
                                    with an error message or None.

                           ``permission_classes``\ *=[]*

                           *async*\ ``post``\ (\ *request*, *uuid*\ )\ `[source] <_modules/apikeys/views.html#RecordVideoVMView.post>`__
                              Asynchronously handle a POST request to
                              start recording a video.

                              This method attempts to start a recording
                              for the specified virtual machine. It
                              checks if the machine exists and if a
                              recording is not already in progress. If
                              these conditions are met, it sets up a new
                              video file and starts the recording. The
                              recording runs for a maximum duration of
                              three hours or until it is manually
                              stopped. After the recording is finished,
                              it cleans up the resources and sends a
                              response indicating success.

                              .. container:: section
                                 :name: id27

                                 .. rubric:: Parameters:
                                    :name: parameters-12

                                 requestdjango.http.HttpRequest
                                    The request instance for the current
                                    request.
                                 uuidstr
                                    The unique identifier for the
                                    virtual machine.

                              .. container:: section
                                 :name: id28

                                 .. rubric:: Returns:
                                    :name: returns-12

                                 JsonResponse
                                    A JsonResponse indicating whether
                                    the recording started successfully
                                    or detailing any errors that
                                    occurred.

                              .. container:: section
                                 :name: id29

                                 .. rubric:: Raises:
                                    :name: raises-1

                                 Exception
                                    Any exception that occurs while
                                    starting or managing the recording.

                        *class*\ ``apikeys.views.``\ ``RecreateFoldersView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#RecreateFoldersView>`__
                           Bases: ``View``

                           This Django view handles POST requests to
                           recreate a set of folders inside a QCOW2 file
                           in a Virtual Machine.

                           The view first authenticates the request
                           based on the provided API key. If the user
                           related to the API key is not active, it
                           returns an error.

                           Upon successful authentication, the view
                           retrieves a list of folders and a VM uuid
                           from the request. It then creates a new QCOW2
                           file in the corresponding VM directory and
                           formats it with NTFS filesystem, followed by
                           creating the specified folders in the root
                           directory of the filesystem. If the QCOW2
                           file already exists, it is first deleted.

                           If the QCOW2 file is created and formatted
                           successfully, the view returns a success
                           message. If an error occurs during the
                           operation, it returns an error message.

                           The view uses the create_and_format_qcow2
                           function to perform the creation and
                           formatting operations.

                           ``authentication_classes``\ *=[]*

                           ``dispatch``\ (\ *request*, *\*args*, *\*\*kwargs*\ )

                           ``permission_classes``\ *=[]*

                           *async*\ ``post``\ (\ *request*\ )\ `[source] <_modules/apikeys/views.html#RecreateFoldersView.post>`__

                        *class*\ ``apikeys.views.``\ ``RemoveVMDateTimeView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#RemoveVMDateTimeView>`__
                           Bases: ``View``

                           View to remove the datetime line from a VM’s
                           configuration.

                           The view has no authentication or permission
                           restrictions. The post method is used to
                           handle the removal of the datetime line from
                           the configuration of a VM with a given UUID.

                           ``authentication_classes``\ *=[]*

                           ``dispatch``\ (\ *request*, *\*args*, *\*\*kwargs*\ )

                           ``permission_classes``\ *=[]*

                           *async*\ ``post``\ (\ *request*\ )\ `[source] <_modules/apikeys/views.html#RemoveVMDateTimeView.post>`__
                              Handle a POST request to remove the
                              datetime line from a VM’s configuration.

                              This method first checks if the user is
                              authenticated or if there is an API key
                              error. If there’s an API key error, it
                              returns a JSON response with the error.
                              The method then retrieves the UUID from
                              the POST data. It locates the .vnc
                              configuration file for the VM with the
                              provided UUID, reads its content, and
                              removes any line containing the ‘-rtc
                              base=’ string. If successful, the method
                              returns a JSON response indicating the
                              successful operation. If there’s an error,
                              it returns a JSON response with the error
                              message.

                              .. container:: section
                                 :name: id30

                                 .. rubric:: Parameters:
                                    :name: parameters-13

                                 requestdjango.http.HttpRequest
                                    The request instance for the current
                                    request.

                              .. container:: section
                                 :name: id31

                                 .. rubric:: Returns:
                                    :name: returns-13

                                 django.http.JsonResponse
                                    A JsonResponse indicating the result
                                    of the operation.

                        *class*\ ``apikeys.views.``\ ``ResetVMView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#ResetVMView>`__
                           Bases: ``View``

                           This Django View handles POST requests to
                           reset a VM. It authenticates the request and
                           then uses the system_reset function to send a
                           reset command to the VM.

                           The VM is identified by its UUID, which
                           should be included in the URL of the request.

                           ``authentication_classes``\ *=[<class 'rest_framework.authentication.SessionAuthentication'>]*

                           ``dispatch``\ (\ *request*, *\*args*, *\*\*kwargs*\ )

                           ``get_user_or_key_error``\ (\ *request*\ )\ `[source] <_modules/apikeys/views.html#ResetVMView.get_user_or_key_error>`__
                              Helper method to retrieve the
                              authenticated user from the request, or
                              return an error response if the request is
                              not authenticated.

                              The request can be authenticated either
                              through session-based authentication or by
                              including an ‘X-API-KEY’ header in the
                              request.

                              Args:
                                 request: The Django request object.
                              Returns:
                                 If the request is authenticated,
                                 returns a tuple where the first element
                                 is the authenticated user and the
                                 second element is None.

                                 If the request is not authenticated,
                                 returns a tuple where the first element
                                 is None and the second element is a
                                 JsonResponse with an error message.

                           ``permission_classes``\ *=[]*

                           *async*\ ``post``\ (\ *request*, *uuid*\ )\ `[source] <_modules/apikeys/views.html#ResetVMView.post>`__
                              This method handles the POST request to
                              reset a VM. It checks for user
                              authentication, verifies the existence of
                              the VM, and then sends the reset command.

                              Args:
                                 request (django.http.HttpRequest): The
                                 request instance. uuid (str): The UUID
                                 of the VM to be reset.
                              Returns:
                                 django.http.JsonResponse: A JSON
                                 response with the result of the
                                 operation.

                        *class*\ ``apikeys.views.``\ ``RollbackSnapshotView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#RollbackSnapshotView>`__
                           Bases: ``View``

                           API View that handles POST requests to
                           rollback a snapshot of a specific VM.

                           This view requires an API key for
                           authentication. If the API key is valid and
                           is associated with an active user, it calls
                           the rollback_snapshot asynchronous function
                           to rollback to the snapshot.

                           If the API key is missing, invalid, or
                           associated with an inactive user, or if the
                           snapshot name is missing in the request data,
                           an error message is returned.

                           The response indicates either a success or an
                           error message in a JSON format: {

                              .. container::

                                 “message”: <string>

                           } or {

                              .. container::

                                 “error”: <string>

                           }

                           ``dispatch``\ (\ *request*, *\*args*, *\*\*kwargs*\ )

                           *async*\ ``post``\ (\ *request*, *uuid*\ )\ `[source] <_modules/apikeys/views.html#RollbackSnapshotView.post>`__
                              Handles the POST request to rollback to a
                              snapshot of a VM.

                              Args:
                                 request: The HTTP request from the client. Expected to contain the API key in the headers,
                                    and the snapshot name in the request
                                    data.

                                 uuid: The UUID of the VM to rollback
                                 the snapshot.

                              Returns:
                                 JsonResponse: A JsonResponse that
                                 either contains a success message or an
                                 error message.

                        *class*\ ``apikeys.views.``\ ``RunPluginView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#RunPluginView>`__
                           Bases: ``APIView``

                           This Django view handles GET requests to run
                           a forensic plugin script on a specified image
                           within a Virtual Machine.

                           The view first authenticates the request
                           based on the provided API key. If the user
                           related to the API key is not active, it
                           returns an error.

                           Upon successful authentication, the view
                           retrieves the plugin directory and VM uuid
                           from the request parameters. It validates the
                           existence of the plugin script and the image,
                           both identified using the provided
                           parameters.

                           If the validation is successful, it attempts
                           to run the plugin script on the image and
                           returns the script’s stdout as the response.
                           If the script fails to run, the error details
                           are returned in the response.

                           If the validation fails because of the
                           non-existence of the plugin script or the
                           image, an appropriate error message is
                           returned.

                           This view does not require any special
                           permissions or authentication classes, as it
                           is intended to be used internally by the
                           system.

                           ``authentication_classes``\ *=[]*

                           ``get``\ (\ *request*\ )\ `[source] <_modules/apikeys/views.html#RunPluginView.get>`__
                              Handles GET requests to execute a specific
                              forensic plugin on a VM image.

                              The method retrieves the API key from the
                              request headers and validates it. If the
                              API key is invalid or belongs to an
                              inactive user, an error response is
                              returned.

                              The method retrieves the plugin directory
                              and image UUID from the GET parameters. It
                              validates these parameters by checking the
                              existence of the plugin script and the
                              image path. If any of these does not
                              exist, an error response is returned.

                              The method looks for the latest
                              ‘.qcow2-sda’ file within the image path
                              and sets it as the target for the plugin.

                              Upon successful validation, the method
                              attempts to run the plugin script on the
                              image using a bash subprocess. The output
                              from the subprocess is returned in the
                              response.

                              If the plugin script execution fails, the
                              error details are returned in the
                              response.

                              Parameters: request (HttpRequest): The
                              request object that has triggered this
                              method.

                              Returns: JsonResponse: A JSON object
                              containing either the output of the plugin
                              execution or an error message.

                           ``permission_classes``\ *=[]*

                        *class*\ ``apikeys.views.``\ ``RunScriptView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#RunScriptView>`__
                           Bases: ``APIView``

                           API endpoint for running a script.

                           This view accepts a POST request and expects
                           an API key to be provided in the request
                           headers. The request should contain a
                           ‘script’ parameter in the data payload, which
                           contains the script to be executed. The
                           script is executed using the subprocess
                           module, and the output and error code are
                           returned in the response.

                           Note: This view does not perform any
                           authentication or permission checks beyond
                           validating the API key.

                           ``authentication_classes``\ *=[]*

                           ``permission_classes``\ *=[]*

                           ``post``\ (\ *request*\ )\ `[source] <_modules/apikeys/views.html#RunScriptView.post>`__
                              Handles the POST request to execute a
                              script.

                              Args:
                                 request: The POST request received by
                                 the server.
                              Returns:
                                 Response: A Django Response object
                                 containing the script output and error
                                 code.

                        *class*\ ``apikeys.views.``\ ``ScreenshotVMView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#ScreenshotVMView>`__
                           Bases: ``View``

                           A View class to handle the capture of
                           screenshots from a Virtual Machine (VM).

                           This View supports an asynchronous POST
                           request, which initiates the capture of a
                           screenshot from the VM. The VM is identified
                           by its UUID, which is passed in the URL.

                           Authentication is required to access this
                           View. It supports both session-based
                           authentication and API key authentication.

                           ``authentication_classes``\ *=[<class 'rest_framework.authentication.SessionAuthentication'>]*

                           ``dispatch``\ (\ *request*, *\*args*, *\*\*kwargs*\ )

                           ``get_user_or_key_error``\ (\ *request*\ )\ `[source] <_modules/apikeys/views.html#ScreenshotVMView.get_user_or_key_error>`__
                              Helper method to retrieve the
                              authenticated user from the request, or
                              return an error response if the request is
                              not authenticated.

                              The request can be authenticated either
                              through session-based authentication or by
                              including an ‘X-API-KEY’ header in the
                              request.

                              Args:
                                 request: The Django request object.
                              Returns:
                                 If the request is authenticated,
                                 returns a tuple where the first element
                                 is the authenticated user and the
                                 second element is None.

                                 If the request is not authenticated,
                                 returns a tuple where the first element
                                 is None and the second element is a
                                 JsonResponse with an error message.

                           ``permission_classes``\ *=[]*

                           *async*\ ``post``\ (\ *request*, *uuid*\ )\ `[source] <_modules/apikeys/views.html#ScreenshotVMView.post>`__
                              Handles a POST request to capture a
                              screenshot from a VM.

                              The VM is identified by its UUID, which is
                              passed in the URL.

                              The request must be authenticated. This
                              can be done either through session-based
                              authentication or by including an
                              ‘X-API-KEY’ header in the request.

                              Args:
                                 request: The Django request object.
                                 uuid: The UUID of the VM.
                              Returns:
                                 A JsonResponse containing the status of
                                 the screenshot operation. If the
                                 operation is successful, the response
                                 will include a ‘screenshot_taken’ key
                                 with a value of True, and a ‘message’
                                 key with the screenshot number.

                                 If an error occurs, the JsonResponse
                                 will contain an ‘error’ key with a
                                 description of the error.

                        *class*\ ``apikeys.views.``\ ``ShutdownVMView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#ShutdownVMView>`__
                           Bases: ``View``

                           This Django View handles POST requests to
                           shutdown a VM. It authenticates the request
                           and then uses the system_shutdown function to
                           send a shutdown command to the VM.

                           The VM is identified by its UUID, which
                           should be included in the URL of the request.

                           ``authentication_classes``\ *=[<class 'rest_framework.authentication.SessionAuthentication'>]*

                           ``dispatch``\ (\ *request*, *\*args*, *\*\*kwargs*\ )

                           ``get_user_or_key_error``\ (\ *request*\ )\ `[source] <_modules/apikeys/views.html#ShutdownVMView.get_user_or_key_error>`__
                              Helper method to retrieve the
                              authenticated user from the request, or
                              return an error response if the request is
                              not authenticated.

                              The request can be authenticated either
                              through session-based authentication or by
                              including an ‘X-API-KEY’ header in the
                              request.

                              Args:
                                 request: The Django request object.
                              Returns:
                                 If the request is authenticated,
                                 returns a tuple where the first element
                                 is the authenticated user and the
                                 second element is None.

                                 If the request is not authenticated,
                                 returns a tuple where the first element
                                 is None and the second element is a
                                 JsonResponse with an error message.

                           ``permission_classes``\ *=[]*

                           *async*\ ``post``\ (\ *request*, *uuid*\ )\ `[source] <_modules/apikeys/views.html#ShutdownVMView.post>`__
                              This method handles the POST request to
                              shut down a VM. It checks for user
                              authentication, verifies the existence of
                              the VM, and then sends the shutdown
                              command.

                              Args:
                                 request (django.http.HttpRequest): The
                                 request instance. uuid (str): The UUID
                                 of the VM to be shutdown.
                              Returns:
                                 django.http.JsonResponse: A JSON
                                 response with the result of the
                                 operation.

                        *class*\ ``apikeys.views.``\ ``SnapshotListView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#SnapshotListView>`__
                           Bases: ``View``

                           API View that handles GET requests to
                           retrieve the list of snapshots of a specific
                           VM.

                           This view requires an API key for
                           authentication. If the API key is valid and
                           is associated with an active user, it calls
                           the get_snapshots asynchronous function to
                           retrieve the list of snapshots.

                           If the API key is missing, invalid, or
                           associated with an inactive user, an error
                           message is returned.

                           The response includes a list of snapshots or
                           an error message in a JSON format: {

                              .. container::

                                 “snapshots”: [<list of snapshots>]

                           } or {

                              .. container::

                                 “error”: <string>

                           }

                           ``dispatch``\ (\ *request*, *\*args*, *\*\*kwargs*\ )

                           *async*\ ``get``\ (\ *request*, *uuid*\ )\ `[source] <_modules/apikeys/views.html#SnapshotListView.get>`__
                              Handles the GET request to retrieve the
                              list of snapshots of a VM.

                              Args:
                                 request: The HTTP request from the
                                 client. Expected to contain the API key
                                 in the headers. uuid: The UUID of the
                                 VM to get the snapshots.
                              Returns:
                                 JsonResponse: A JsonResponse that
                                 either contains the list of snapshots
                                 or an error message.

                        *class*\ ``apikeys.views.``\ ``StartTapInterfaceView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#StartTapInterfaceView>`__
                           Bases: ``View``

                           View to start the tap interface of a VM.

                           The view authenticates the user with
                           SessionAuthentication. The post method is
                           used to handle the start request of the tap
                           interface of a VM.

                           ``authentication_classes``\ *=[<class 'rest_framework.authentication.SessionAuthentication'>]*

                           ``dispatch``\ (\ *request*, *\*args*, *\*\*kwargs*\ )

                           ``permission_classes``\ *=[]*

                           *async*\ ``post``\ (\ *request*\ )\ `[source] <_modules/apikeys/views.html#StartTapInterfaceView.post>`__
                              Handle a POST request to start the tap
                              interface of a VM.

                              This method first checks if there is an
                              API key error. If there’s an API key
                              error, it returns a JSON response with the
                              error. The method then gets the UUID from
                              the POST data and tries to start the tap
                              interface. It executes shell commands to
                              get the tap interface and starts it. If
                              the tap interface starts successfully, the
                              method returns a JSON response with a
                              positive message. If there’s an error
                              while starting the tap interface, the
                              method returns a JSON response with the
                              error.

                              .. container:: section
                                 :name: id32

                                 .. rubric:: Parameters:
                                    :name: parameters-14

                                 requestdjango.http.HttpRequest
                                    The request instance for the current
                                    request.

                              .. container:: section
                                 :name: id33

                                 .. rubric:: Returns:
                                    :name: returns-14

                                 django.http.JsonResponse
                                    A JsonResponse with a message about
                                    the status of the tap interface
                                    start action.

                        *class*\ ``apikeys.views.``\ ``StartVMView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#StartVMView>`__
                           Bases: ``APIView``

                           API endpoint that allows VMs to be started
                           via POST requests.

                           This view accepts a POST request with a UUID
                           and attempts to start the corresponding VM.
                           If successful, it returns a 200 OK response
                           with a JSON body indicating the VM has been
                           started and provides the VNC and WebSocket
                           ports. If the VM path or VNC script cannot be
                           found, it returns a 404 Not Found error. An
                           API key or session-based authentication is
                           required.

                           ``authentication_classes``\ *=[<class 'rest_framework.authentication.SessionAuthentication'>]*

                           ``permission_classes``\ *=[]*

                           ``post``\ (\ *request*, *uuid*\ )\ `[source] <_modules/apikeys/views.html#StartVMView.post>`__
                              Starts the VM specified by the UUID.

                              Args:
                                 request: The POST request received by
                                 the server. uuid: The UUID of the VM to
                                 be started.
                              Returns:
                                 Response: A Django Response object.

                        *class*\ ``apikeys.views.``\ ``StopTapInterfaceView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#StopTapInterfaceView>`__
                           Bases: ``View``

                           View to stop the tap interface of a VM.

                           The view authenticates the user with
                           SessionAuthentication. The post method is
                           used to handle the stop request of the tap
                           interface of a VM.

                           ``authentication_classes``\ *=[<class 'rest_framework.authentication.SessionAuthentication'>]*

                           ``dispatch``\ (\ *request*, *\*args*, *\*\*kwargs*\ )

                           ``permission_classes``\ *=[]*

                           *async*\ ``post``\ (\ *request*\ )\ `[source] <_modules/apikeys/views.html#StopTapInterfaceView.post>`__
                              Handle a POST request to stop the tap
                              interface of a VM.

                              This method first checks if there is an
                              API key error. If there’s an API key
                              error, it returns a JSON response with the
                              error. The method then gets the UUID from
                              the POST data and tries to stop the tap
                              interface. It executes shell commands to
                              get the tap interface and stops it. If the
                              tap interface stops successfully, the
                              method returns a JSON response with a
                              positive message. If there’s an error
                              while stopping the tap interface, the
                              method returns a JSON response with the
                              error.

                              .. container:: section
                                 :name: id34

                                 .. rubric:: Parameters:
                                    :name: parameters-15

                                 requestdjango.http.HttpRequest
                                    The request instance for the current
                                    request.

                              .. container:: section
                                 :name: id35

                                 .. rubric:: Returns:
                                    :name: returns-15

                                 django.http.JsonResponse
                                    A JsonResponse with a message about
                                    the status of the tap interface stop
                                    action.

                        *class*\ ``apikeys.views.``\ ``StopVMView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#StopVMView>`__
                           Bases: ``APIView``

                           API endpoint that allows VMs to be stopped
                           via POST requests.

                           This view accepts a POST request with a UUID
                           and attempts to stop the corresponding screen
                           session of the VM. If successful, it returns
                           a 200 OK response with a JSON body indicating
                           the VM has been stopped. If the screen
                           session cannot be found, it returns a 404 Not
                           Found error. An API key is required for
                           authentication.

                           ``authentication_classes``\ *=[<class 'rest_framework.authentication.SessionAuthentication'>]*

                           ``permission_classes``\ *=[]*

                           ``post``\ (\ *request*, *uuid*\ )\ `[source] <_modules/apikeys/views.html#StopVMView.post>`__
                              Stops the VM specified by the UUID.

                              Args:
                                 request: The POST request received by
                                 the server. uuid: The UUID of the VM to
                                 be stopped.
                              Returns:
                                 Response: A Django Response object.

                        *class*\ ``apikeys.views.``\ ``StopVideoRecordingVMView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#StopVideoRecordingVMView>`__
                           Bases: ``View``

                           View to handle the stoppage of video
                           recording.

                           The view uses session authentication and has
                           no permission restrictions. The post method
                           is used to handle the stoppage of the video
                           recording for a VM with a given UUID.

                           ``authentication_classes``\ *=[<class 'rest_framework.authentication.SessionAuthentication'>]*

                           ``dispatch``\ (\ *request*, *\*args*, *\*\*kwargs*\ )

                           ``get_user_or_key_error``\ (\ *request*\ )\ `[source] <_modules/apikeys/views.html#StopVideoRecordingVMView.get_user_or_key_error>`__
                              Check if the user is authenticated or if
                              there is an API key error.

                              This method checks if the user associated
                              with the request is authenticated. If the
                              user is not authenticated, it checks if
                              there’s an API key in the request. If the
                              API key is valid and associated with an
                              active user, the method returns this user.
                              If the API key is not valid or the user is
                              not active, it returns a JSON response
                              with the corresponding error. If there’s
                              no API key at all, it returns a JSON
                              response indicating that the API key is
                              required.

                              .. container:: section
                                 :name: id36

                                 .. rubric:: Parameters:
                                    :name: parameters-16

                                 requestdjango.http.HttpRequest
                                    The request instance for the current
                                    request.

                              .. container:: section
                                 :name: id37

                                 .. rubric:: Returns:
                                    :name: returns-16

                                 tuple
                                    A tuple where the first element is
                                    the authenticated user or None, and
                                    the second element is a JsonResponse
                                    with an error message or None.

                           ``permission_classes``\ *=[]*

                           *async*\ ``post``\ (\ *request*, *uuid*\ )\ `[source] <_modules/apikeys/views.html#StopVideoRecordingVMView.post>`__
                              Handle a POST request to stop video
                              recording for a VM with a given UUID.

                              This method first checks if the user is
                              authenticated or if there is an API key
                              error. If there’s an API key error, it
                              returns a JSON response with the error. If
                              the UUID is present in the recordings, it
                              stops the recording by setting the
                              corresponding value to False. If the UUID
                              is not present, it returns a HTTP 400
                              error. Finally, it returns a JSON response
                              confirming the stoppage of the recording.

                              .. container:: section
                                 :name: id38

                                 .. rubric:: Parameters:
                                    :name: parameters-17

                                 requestdjango.http.HttpRequest
                                    The request instance for the current
                                    request.
                                 uuidstr
                                    The UUID of the VM for which the
                                    recording should be stopped.

                              .. container:: section
                                 :name: id39

                                 .. rubric:: Returns:
                                    :name: returns-17

                                 django.http.JsonResponse
                                    A JsonResponse indicating the result
                                    of the operation.

                        *class*\ ``apikeys.views.``\ ``UploadISOView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/apikeys/views.html#UploadISOView>`__
                           Bases: ``View``

                           This is a Django view that provides an
                           endpoint for uploading an ISO file to a
                           specified directory.

                           The UploadISOView class handles HTTP POST
                           requests to receive an ISO file and save it
                           to the directory.

                           The class uses Django’s View, which means it
                           can handle different types of HTTP requests.
                           It currently only implements handling of POST
                           requests via the defined post() method.

                           Attributes:
                              authentication_classes (list): A list of
                              authentication classes the view should
                              use. It’s empty in this case.
                              permission_classes (list): A list of
                              permissions the view should enforce. It’s
                              empty in this case.

                           ``authentication_classes``\ *=[]*

                           ``dispatch``\ (\ *request*, *\*args*, *\*\*kwargs*\ )

                           ``permission_classes``\ *=[]*

                           ``post``\ (\ *request*\ )\ `[source] <_modules/apikeys/views.html#UploadISOView.post>`__
                              This method handles the POST request to
                              upload an ISO file.

                              It first validates the API key from the
                              request. If the API key is valid and
                              belongs to an active user, it checks if an
                              ISO file is provided in the request. If it
                              is, it saves the ISO file to a specified
                              directory and returns a confirmation
                              message.

                              Parameters: request (HttpRequest): The
                              request object that has triggered this
                              method.

                              Returns: JsonResponse: A JSON object
                              containing a confirmation message or an
                              error message with an HTTP status code.

                        ``apikeys.views.``\ ``change_qcow2``\ (\ *qcow2_file*, *folders*\ )\ `[source] <_modules/apikeys/views.html#change_qcow2>`__
                           This function creates new folders in a qcow2
                           disk image. It uses guestfish commands to
                           interact with the disk image.

                           Parameters: qcow2_file (str): Path to the
                           qcow2 file that should be changed. folders
                           (list): List of folder names to be created in
                           the qcow2 image.

                           Returns: None

                           Raises: subprocess.CalledProcessError: If a
                           guestfish command fails.

                        ``apikeys.views.``\ ``create_and_format_qcow2``\ (\ *qcow2_file*, *folders*\ )\ `[source] <_modules/apikeys/views.html#create_and_format_qcow2>`__
                           Creates and formats a new QCOW2 file with a
                           capacity of 20GB, and initializes it with a
                           new NTFS partition.

                           This function first creates a new QCOW2 file
                           using the qemu-img command. Then, it
                           initializes a new NTFS partition on the QCOW2
                           file using the guestfish command-line tool.

                           After the partition is created, the function
                           creates a series of folders in the root
                           directory of the partition. Finally, it
                           writes a readme file in the root directory of
                           the partition.

                           Args:
                              qcow2_file (str): The path where the new
                              QCOW2 file will be created. folders
                              (list): A list of folder names that will
                              be created in the root directory of the
                              NTFS partition.
                           Raises:
                              subprocess.CalledProcessError: If the
                              qemu-img command or the guestfish command
                              fails.

                        *async*\ ``apikeys.views.``\ ``create_snapshot``\ (\ *uuid*\ )\ `[source] <_modules/apikeys/views.html#create_snapshot>`__
                           Asynchronously creates a snapshot of a
                           specific VM.

                           This function uses QEMU’s QMP (QEMU Machine
                           Protocol) to execute commands on the VM. It
                           specifically runs the savevm command to
                           create the snapshot.

                           Args:
                              uuid (str): The unique identifier for the
                              VM.
                           Returns:
                              str: The name of the snapshot if
                              successful, or an error message if an
                              exception occurred.

                        *async*\ ``apikeys.views.``\ ``create_video``\ (\ *uuid*, *output_video_path*\ )\ `[source] <_modules/apikeys/views.html#create_video>`__
                           Asynchronously create a video from
                           screenshots taken in a virtual machine using
                           QEMU Machine Protocol (QMP).

                           The function connects to QMP, executes a
                           screendump command to take a screenshot and
                           saves it to a specified path. It then reads
                           the screenshot into an image and writes the
                           image as a frame to a video file. If the
                           video writer is not yet set up, it
                           initializes it with the size of the first
                           frame. Once the frame has been written to the
                           video, it removes the screenshot file.

                           .. container:: section
                              :name: id40

                              .. rubric:: Parameters:
                                 :name: parameters-18

                              uuidstr
                                 The unique identifier for the video
                                 file’s directory.
                              output_video_pathstr
                                 The path where the output video will be
                                 saved.

                           .. container:: section
                              :name: id41

                              .. rubric:: Raises:
                                 :name: raises-2

                              Exception
                                 Any exception that occurs while
                                 creating the video or
                                 connecting/disconnecting from QMP.

                        *async*\ ``apikeys.views.``\ ``delete_snapshot``\ (\ *uuid*, *snapshot_name*\ )\ `[source] <_modules/apikeys/views.html#delete_snapshot>`__
                           Asynchronously delete a snapshot of a
                           specific VM.

                           This function uses QEMU’s QMP (QEMU Machine
                           Protocol) to execute commands on the VM. It
                           specifically runs the delvm command to delete
                           the snapshot.

                           Args:
                              uuid (str): The unique identifier for the
                              VM. snapshot_name (str): The name of the
                              snapshot to delete.
                           Returns:
                              str: A message indicating whether the
                              snapshot was successfully deleted or not.

                        *async*\ ``apikeys.views.``\ ``eject_cdrom``\ (\ *uuid*\ )\ `[source] <_modules/apikeys/views.html#eject_cdrom>`__
                           Asynchronously ejects the CD-ROM from a
                           specified virtual machine.

                           This function establishes a connection to the
                           QEMU Machine Protocol (QMP) and sends a
                           command to open the tray of the CD-ROM drive,
                           effectively ejecting the CD-ROM.

                           Parameters: uuid (str): The unique identifier
                           of the virtual machine.

                           Returns: str: A confirmation message.

                        ``apikeys.views.``\ ``find_available_port``\ (\ *start_port*\ )\ `[source] <_modules/apikeys/views.html#find_available_port>`__
                           This function finds two available, sequential
                           TCP ports to use, starting from the given
                           start_port.

                           Args:
                              start_port (int): The port number from
                              which to start checking for availability.
                           Returns:
                              tuple: A pair of two available, sequential
                              TCP port numbers.
                           Raises:
                              OSError: If an error occurs that is not
                              related to a port being in use (e.g.,
                              permission denied, etc.)

                        ``apikeys.views.``\ ``generate_random_mac_address``\ ()\ `[source] <_modules/apikeys/views.html#generate_random_mac_address>`__
                           Generates a random MAC address.

                           This function creates a MAC address with the
                           locally administered and unicast bits set,
                           and with the rest of the bits randomized.

                           Returns: str: The generated MAC address.

                        ``apikeys.views.``\ ``get_available_memory``\ ()\ `[source] <_modules/apikeys/views.html#get_available_memory>`__
                           Get the current available system memory.

                           This function uses the psutil library to
                           fetch system memory information. It returns
                           the amount of available memory in Megabytes.

                           .. container:: section
                              :name: id42

                              .. rubric:: Returns:
                                 :name: returns-18

                              float
                                 The amount of available system memory
                                 in Megabytes.

                        ``apikeys.views.``\ ``get_plugin_info``\ (\ *plugin_dir*, *info*\ )\ `[source] <_modules/apikeys/views.html#get_plugin_info>`__
                           Runs the ‘info’ command of the plugin script
                           and retrieves the specified information.

                           Parameters: plugin_dir (str): The directory
                           where the plugin script is located. info
                           (str): The type of information to retrieve
                           (e.g. ‘plugin_name’, ‘plugin_description’).

                           Returns: str: The requested information, or
                           an empty string if the information could not
                           be retrieved.

                        *async*\ ``apikeys.views.``\ ``get_snapshots``\ (\ *uuid*\ )\ `[source] <_modules/apikeys/views.html#get_snapshots>`__
                           Asynchronously retrieves the list of
                           snapshots of a specific VM.

                           This function uses QEMU’s QMP (QEMU Machine
                           Protocol) to execute commands on the VM. It
                           specifically runs the info snapshots command
                           to retrieve the list of snapshots.

                           Args:
                              uuid (str): The unique identifier for the
                              VM.
                           Returns:
                              list: A list of dictionaries containing snapshot information. Each dictionary includes
                                 snapshot id, tag, VM size, date, and VM
                                 clock. If an exception occurred, an
                                 empty list is returned.

                        *async*\ ``apikeys.views.``\ ``insert_cdrom``\ (\ *uuid*, *filename*\ )\ `[source] <_modules/apikeys/views.html#insert_cdrom>`__
                           Asynchronously inserts a CD-ROM into a
                           specified virtual machine.

                           This function establishes a connection to the
                           QEMU Machine Protocol (QMP) and sends a
                           command to change the medium of the CD-ROM
                           drive to the specified ISO file.

                           Parameters: uuid (str): The unique identifier
                           of the virtual machine. filename (str): The
                           name of the ISO file to insert into the
                           CD-ROM drive.

                           Returns: str: A confirmation message.

                        *async*\ ``apikeys.views.``\ ``insert_network_card``\ (\ *uuid*, *mac_address=None*\ )\ `[source] <_modules/apikeys/views.html#insert_network_card>`__
                           Asynchronously inserts a network card into a
                           specified virtual machine.

                           This function first generates a random MAC
                           address if none is provided. It then
                           establishes a connection to the QEMU Machine
                           Protocol (QMP) and sends commands to add a
                           new network device to the machine.

                           Parameters: uuid (str): The unique identifier
                           of the virtual machine. mac_address (str,
                           optional): The MAC address to assign to the
                           network card.

                           Returns: str: A confirmation message.

                        *async*\ ``apikeys.views.``\ ``memory_snapshot``\ (\ *uuid*\ )\ `[source] <_modules/apikeys/views.html#memory_snapshot>`__
                           This asynchronous function captures a
                           snapshot of a VM’s memory.

                           It establishes a connection with the QEMU
                           Machine Protocol (QMP) running on the VM,
                           then uses the QMP command ‘dump-guest-memory’
                           to capture the memory snapshot.

                           The function saves the memory snapshot to the
                           VM’s directory, with a unique filename based
                           on the current number of existing snapshots.

                           Parameters: uuid (str): The UUID of the VM.

                           Returns: str: The path to the newly created
                           memory snapshot file.

                           Raises: Exception: If there’s an error
                           executing the ‘dump-guest-memory’ command or
                           disconnecting from QMP.

                        *async*\ ``apikeys.views.``\ ``rollback_snapshot``\ (\ *uuid*, *snapshot_name*\ )\ `[source] <_modules/apikeys/views.html#rollback_snapshot>`__
                           Asynchronously rollback to a snapshot of a
                           specific VM.

                           This function uses QEMU’s QMP (QEMU Machine
                           Protocol) to execute commands on the VM. It
                           specifically runs the loadvm command to
                           rollback to the snapshot.

                           Args:
                              uuid (str): The unique identifier for the
                              VM. snapshot_name (str): The name of the
                              snapshot to rollback to.
                           Returns:
                              str: A message indicating whether the
                              snapshot was successfully rolled back or
                              not.

                        *async*\ ``apikeys.views.``\ ``screendump``\ (\ *uuid*\ )\ `[source] <_modules/apikeys/views.html#screendump>`__
                           Capture a screenshot of a Virtual Machine
                           (VM) and save it as a PNG file.

                           This function uses the QEMU Machine Protocol
                           (QMP) to communicate with the VM and issue
                           the ‘screendump’ command, which captures a
                           screenshot of the current state of the VM’s
                           display. The screenshot is saved to a
                           directory named ‘screenshots’ within the VM’s
                           directory, and the file is named ‘sc’
                           followed by a five-digit number, with leading
                           zeroes as necessary.

                           Args:
                              uuid: The UUID of the VM to capture a
                              screenshot from.
                           Returns:
                              The number of the screenshot that was
                              taken, as an integer.
                           Raises:
                              Prints an exception error if the QMP
                              connection or command execution fails.

                        *async*\ ``apikeys.views.``\ ``system_reset``\ (\ *uuid*\ )\ `[source] <_modules/apikeys/views.html#system_reset>`__
                           This function sends a reset command to a VM
                           specified by its UUID. It uses QEMU’s QMP
                           (QEMU Machine Protocol) to interact with the
                           VM.

                           Args:
                              uuid (str): The UUID of the VM to be
                              reset.
                           Raises:
                              Exception: If there’s an error while
                              trying to interact with the VM, an
                              exception will be raised.

                        *async*\ ``apikeys.views.``\ ``system_shutdown``\ (\ *uuid*\ )\ `[source] <_modules/apikeys/views.html#system_shutdown>`__
                           This function sends a shutdown command to a
                           VM specified by its UUID. It uses QEMU’s QMP
                           (QEMU Machine Protocol) to interact with the
                           VM.

                           Args:
                              uuid (str): The UUID of the VM to be
                              shutdown.
                           Raises:
                              Exception: If there’s an error while
                              trying to interact with the VM, an
                              exception will be raised.

                        ``apikeys.views.``\ ``validate_date``\ (\ *date_str*\ )\ `[source] <_modules/apikeys/views.html#validate_date>`__
                           Function to validate the date string against
                           the format ‘YYYY-MM-DDTHH:MM:SS’

                     .. container:: section
                        :name: module-apikeys

                        .. rubric:: Module contents
                           :name: module-contents

            --------------

            .. container::

               © Copyright 2023, Nuno Mourinho.

            Built with `Sphinx <https://www.sphinx-doc.org/>`__ using a
            `theme <https://github.com/readthedocs/sphinx_rtd_theme>`__
            provided by `Read the Docs <https://readthedocs.org>`__.
