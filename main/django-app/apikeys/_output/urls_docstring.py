@method_decorator(csrf_exempt, name='dispatch')
class ChangeMemorySizeView(View):
    """
    API View that handles POST requests to change the memory size of a Virtual Machine (VM).

    This view requires an API key for authentication and a POST body containing a new memory size.
    If the API key is valid and is associated with an active user, and the POST body contains a valid
    memory size, the script files in the VM directory are updated with the new memory size.

    If the API key is missing, invalid, or associated with an inactive user, or if the memory size
    is invalid, an error message is returned.

    The response indicates whether the memory size update was successful or not in a JSON format:
    {
        "message": <string>
    }
    """
    def post(self, request, uuid):
        """
        Handles the POST request to change the memory size of a VM.

        Args:
            request: The HTTP request from the client. Expected to contain the API key in the headers and the new
                     memory size in the POST body.
            uuid: The UUID of the VM whose memory size is to be changed.

        Returns:
            JsonResponse: A JsonResponse that either contains a success message or an error message.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key:
            try:
                api_key = ApiKey.objects.get(key=api_key)
                user = api_key.user
                if not user.is_active:
                    return JsonResponse({'error': 'User account is disabled.'}, status=401)
            except ApiKey.DoesNotExist:
                return JsonResponse({'error': 'Invalid API key'}, status=401)
        else:
            return JsonResponse({'error': 'API key required'}, status=401)

        vm_path = f"/forensicVM/mnt/vm/{uuid}"
        if not os.path.exists(vm_path):
            return JsonResponse({'error': f'Path for UUID {uuid} not found'}, status=404)

        script_files = glob.glob(os.path.join(vm_path, '*.sh'))
        if not script_files:
            return JsonResponse({'error': f'No script files found for UUID {uuid}'}, status=404)

        recent_script_file = max(script_files, key=os.path.getctime)

        with open(recent_script_file, 'r') as f:
            script_content = f.read()

        memory_pattern = r'-m\s+(\d+)'
        new_memory_size = request.POST.get('memory_size')

        if new_memory_size:
            # Update the memory parameter in the script content
            updated_script_content = re.sub(memory_pattern, f'-m {new_memory_size}', script_content)
            # Write the updated script content back to the file
            with open(recent_script_file, 'w') as f:
                f.write(updated_script_content)

            return JsonResponse({'message': 'Memory size updated successfully'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid or missing memory_size parameter'}, status=400)
    """API View that handles POST requests to change the memory size of a Virtual Machine (VM).

This view requires an API key for authentication and a POST body containing a new memory size.
If the API key is valid and is associated with an active user, and the POST body contains a valid
memory size, the script files in the VM directory are updated with the new memory size.

If the API key is missing, invalid, or associated with an inactive user, or if the memory size
is invalid, an error message is returned.

The response indicates whether the memory size update was successful or not in a JSON format:
{
    "message": <string>
}"""

@method_decorator(csrf_exempt, name='dispatch')
class ChangeVMDateTimeView(View):
    """
    View to change the datetime in a VM's configuration.

    The view has no authentication or permission restrictions.
    The post method is used to handle the updating of the datetime in the configuration of a VM with a given UUID.
    """
    authentication_classes = []
    permission_classes = []

    async def post(self, request):
        """
        Handle a POST request to change the datetime in a VM's configuration.

        This method first checks if there is an API key error.
        If there's an API key error, it returns a JSON response with the error.
        The method then retrieves the UUID and the datetime from the POST data and validates the datetime format.
        If the datetime format is invalid, it returns a JSON response indicating the error.
        It locates the .sh configuration file for the VM with the provided UUID, reads its content, and changes or adds a line with the '-rtc base=' string and the new datetime.
        If successful, the method returns a JSON response indicating the successful operation.
        If there's an error, it returns a JSON response with the error message.

        Parameters:
        ----------
        request : django.http.HttpRequest
            The request instance for the current request.

        Returns:
        -------
        django.http.JsonResponse
            A JsonResponse indicating the result of the operation.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key:
            try:
                api_key = await sync_to_async(ApiKey.objects.get)(key=api_key)
                user = await sync_to_async(getattr)(api_key, 'user')
                if not user.is_active:
                    return JsonResponse({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return JsonResponse({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)



        # Get the UUID and datetime from the POST data
        uuid = request.POST.get('uuid')
        datetime_str = request.POST.get('datetime')

        # Validate the datetime
        if not validate_date(datetime_str):
            return JsonResponse({'error': 'Invalid datetime format'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get the .sh file path
            vnc_file_path = glob.glob(f"/forensicVM/mnt/vm/{uuid}/*vnc.sh")[0]

            # Read the content of the file
            with open(vnc_file_path, 'r') as file:
                lines = file.readlines()

            # Add the new line after the -vga section if it doesn't exist
            for i, line in enumerate(lines):
                if '-vga' in line:
                    if '-rtc base=' not in lines[i+1]:
                        lines.insert(i+1, f'    -rtc base={datetime_str} \\\n')
                    else:
                        lines[i+1]=f'    -rtc base={datetime_str} \\\n'
                    break

            # Write the changes back to the file
            with open(vnc_file_path, 'w') as file:
                file.writelines(lines)

            return JsonResponse({'message': f'Date time {datetime_str} set successfully for VM {uuid}'}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': f'Error updating VM date time: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    """View to change the datetime in a VM's configuration.

The view has no authentication or permission restrictions.
The post method is used to handle the updating of the datetime in the configuration of a VM with a given UUID."""

@method_decorator(csrf_exempt, name='dispatch')
class CheckRecordingStatusVMView(View):
    """
    View to check the status of video recording.

    The view uses session authentication and has no permission restrictions.
    The get method is used to handle the checking of the video recording status for a VM with a given UUID.
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = []

    async def get(self, request, uuid):
        """
        Handle a GET request to check video recording status for a VM with a given UUID.

        This method first checks if the user is authenticated or if there is an API key error.
        If there's an API key error, it returns a JSON response with the error.
        If the UUID is present in the recordings and is recording, it returns a JSON response indicating the recording is in progress.
        If the UUID is not present or not recording, it returns a JSON response indicating no recording is in progress.

        Parameters:
        ----------
        request : django.http.HttpRequest
            The request instance for the current request.
        uuid : str
            The UUID of the VM for which the recording status should be checked.

        Returns:
        -------
        django.http.JsonResponse
            A JsonResponse indicating the result of the operation.
        """
        user, api_key_error = await sync_to_async(self.get_user_or_key_error)(request)
        if api_key_error:
            return api_key_error

        if uuid in recordings and recordings[uuid]:
            result = {'is_recording': True, 'message': f'Recording is in progress for VM with UUID {uuid}'}
        else:
            result = {'is_recording': False, 'message': f'No recording is in progress for VM with UUID {uuid}'}

        return JsonResponse(result, status=status.HTTP_200_OK)

    def get_user_or_key_error(self, request):
        """
        Check if the user is authenticated or if there is an API key error.

        This method checks if the user associated with the request is authenticated.
        If the user is not authenticated, it checks if there's an API key in the request.
        If the API key is valid and associated with an active user, the method returns this user.
        If the API key is not valid or the user is not active, it returns a JSON response with the corresponding error.
        If there's no API key at all, it returns a JSON response indicating that the API key is required.

        Parameters:
        ----------
        request : django.http.HttpRequest
            The request instance for the current request.

        Returns:
        -------
        tuple
            A tuple where the first element is the authenticated user or None,
            and the second element is a JsonResponse with an error message or None.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            print("DEBUG: USER AUTHENTICATED")
        elif api_key:
            try:
                api_key = ApiKey.objects.get(key=api_key)
                user = getattr(api_key, 'user')
                if not user.is_active:
                    return None, JsonResponse({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return None, JsonResponse({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return None, JsonResponse({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)
        return user, None
    """View to check the status of video recording.

The view uses session authentication and has no permission restrictions.
The get method is used to handle the checking of the video recording status for a VM with a given UUID."""

@method_decorator(csrf_exempt, name='dispatch')
class CheckTapInterfaceView(View):
    """
    View to check the status of the tap interface of a VM.

    The view has no authentication or permission restrictions.
    The post method is used to handle the status checking of the tap interface of a VM.
    """
    authentication_classes = []
    permission_classes = []

    async def post(self, request):
        """
        Handle a POST request to check the status of the tap interface of a VM.

        This method first checks if there is an API key error.
        If there's an API key error, it returns a JSON response with the error.
        The method then gets the UUID from the POST data and checks the status of the tap interface.
        It executes shell commands to get the tap interface and checks its status.
        If the tap interface is up, the method returns a JSON response with a positive status and message.
        If the tap interface is down, the method returns a JSON response with a negative status and message.

        Parameters:
        ----------
        request : django.http.HttpRequest
            The request instance for the current request.

        Returns:
        -------
        django.http.JsonResponse
            A JsonResponse with the status and message about the status of the tap interface.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key:
            try:
                api_key = await sync_to_async(ApiKey.objects.get)(key=api_key)
                user = await sync_to_async(getattr)(api_key, 'user')
                if not user.is_active:
                    return JsonResponse({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return JsonResponse({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)

        # Get the uuid from the POST data
        uuid = request.POST.get('uuid')

        if not uuid:
            return JsonResponse({'error': 'UUID required'}, status=status.HTTP_400_BAD_REQUEST)

        # Execute the command to get the tap interface
        cmd = f"ps -ef | grep qemu | grep {uuid}"
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()

        if error:
            return JsonResponse({'error': f'Error finding QEMU process: {error}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        tap_interface = output.decode().split('-netdev tap,id=u1,ifname=')[1].split(',')[0]

        # Check the status of the tap interface
        check_tap_cmd = f"ifconfig {tap_interface}"
        check_tap_process = subprocess.Popen(check_tap_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        check_tap_output, check_tap_error = check_tap_process.communicate()

        if check_tap_error:
            return JsonResponse({'error': f'Error checking tap interface: {check_tap_error}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        is_up = 'UP' in check_tap_output.decode()

        if is_up:
            return JsonResponse({'message': f'Tap interface {tap_interface} is up', 'status': True}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'message': f'Tap interface {tap_interface} is down', 'status': False}, status=status.HTTP_200_OK)
    """View to check the status of the tap interface of a VM.

The view has no authentication or permission restrictions.
The post method is used to handle the status checking of the tap interface of a VM."""

class CheckUserAuthenticatedView(View):
    """
    A Django View class for checking if a user is authenticated.

    This class uses SessionAuthentication for user authentication.
    It doesn't implement any specific permission classes.

    Attributes:
    ----------
    authentication_classes : list
        List of authentication classes the view uses. Here, it's SessionAuthentication.
    permission_classes : list
        List of permission classes the view uses. Here, it's an empty list.

    Methods:
    -------
    get(request):
        Returns a JsonResponse indicating if a user is authenticated.
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = []

    def get(self, request):
        """
        Handles GET request to the view.

        This method retrieves a user from the request or an API key error if one occurred.
        It then checks if the user is authenticated by checking if any API key error occurred.
        If the user is authenticated, it returns a JSON response with the 'authenticated' key set to True.

        Parameters:
        ----------
        request : django.http.HttpRequest
            The request instance for the current request.

        Returns:
        -------
        django.http.JsonResponse
            A JsonResponse that indicates if the user is authenticated.
        """
        user, api_key_error = self.get_user_or_key_error(request)
        if api_key_error:
            return api_key_error
        else:
            return JsonResponse({'authenticated': True}, status=status.HTTP_200_OK)

    def get_user_or_key_error(self, request):
        """
        Retrieves the authenticated user from the request or returns an API key error.

        This method attempts to get an authenticated user from the request.
        If the user is authenticated, it will return the user and None for the error.
        If the user is not authenticated, it will attempt to authenticate the user using an API key provided in the request.
        If the API key is valid and associated with an active user, it returns the user and None for the error.
        If the API key is invalid or the user associated with the key is not active, it returns None for the user and a JsonResponse indicating the error.
        If no API key is provided in the request, it returns None for the user and a JsonResponse indicating that an API key is required.

        Parameters:
        ----------
        request : django.http.HttpRequest
            The request instance for the current request.

        Returns:
        -------
        tuple
            A tuple where the first element is the authenticated user or None if no user could be authenticated,
            and the second element is None or a JsonResponse containing an error message.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            print("DEBUG: USER AUTHENTICATED")
        elif api_key:
            try:
                api_key = ApiKey.objects.get(key=api_key)
                user = getattr(api_key, 'user')
                if not user.is_active:
                    return None, JsonResponse({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return None, JsonResponse({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return None, JsonResponse({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)
        return user, None
    """A Django View class for checking if a user is authenticated.

This class uses SessionAuthentication for user authentication.
It doesn't implement any specific permission classes.

Attributes:
----------
authentication_classes : list
    List of authentication classes the view uses. Here, it's SessionAuthentication.
permission_classes : list
    List of permission classes the view uses. Here, it's an empty list.

Methods:
-------
get(request):
    Returns a JsonResponse indicating if a user is authenticated."""

class CheckVMExistsView(APIView):
    """
    This Django View handles GET requests to check if a VM exists. It authenticates the request and then checks the
    existence of the specified VM's directory in the filesystem.

    The VM is identified by its UUID, which should be included in the URL of the request.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, uuid):
        """
        This method handles the GET request to check if a VM exists. It checks for user authentication, verifies the
        existence of the VM, and then returns a JSON response with the result.

        Args:
            request (django.http.HttpRequest): The request instance.
            uuid (str): The UUID of the VM to be checked.

        Returns:
            rest_framework.response.Response: A JSON response indicating whether the VM exists.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key:
            try:
                api_key = ApiKey.objects.get(key=api_key)
                user = api_key.user
                if not user.is_active:
                    return Response({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return Response({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)

        vm_path = f"/forensicVM/mnt/vm/{uuid}/mode"
        vm_exists = os.path.exists(vm_path)

        result = {'vm_exists': vm_exists}

        return Response(result, status=status.HTTP_200_OK)
    """This Django View handles GET requests to check if a VM exists. It authenticates the request and then checks the
existence of the specified VM's directory in the filesystem.

The VM is identified by its UUID, which should be included in the URL of the request."""

@method_decorator(csrf_exempt, name='dispatch')

class CreateFoldersView(View):
    """
      This class-based view handles the POST request to create specified folders in a qcow2 disk image.

      The method checks the validity and activity status of the provided API key. If the API key is invalid or
      belongs to an inactive user, it returns an error message.

      It then retrieves the list of folders and the UUID path from the request data. It uses the UUID path to form
      the path to the qcow2 file.

      It checks if the qcow2 file exists. If it doesn't, it returns an error.

      It calls the change_qcow2 function to create the folders in the qcow2 file. If successful, it returns a success
      message. If an error occurs, it returns an error message.

      Attributes:
      authentication_classes (list): A list of authentication classes to use for the view.
      permission_classes (list): A list of permission classes to use for the view.

      Methods:
      post(request): Asynchronously handles the POST request.
      """
    authentication_classes = []
    permission_classes = []

    async def post(self, request):
        """
        Asynchronously handles the POST request to create folders in a qcow2 file.

        Parameters:
        request (HttpRequest): The request object that has triggered this method.

        Returns:
        JsonResponse: A JSON object containing a success message if the folders were created successfully,
                       or an error message otherwise.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key:
            try:
                api_key = await sync_to_async(ApiKey.objects.get)(key=api_key)
                user = await sync_to_async(getattr)(api_key, 'user')
                if not user.is_active:
                    return JsonResponse({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return JsonResponse({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)

        # Get the list of folders from the POST data
        folders = request.POST.getlist('folders')
        uuid_path = request.POST.get('uuid_path')
        qcow2_file = f"/forensicVM/mnt/vm/{uuid_path}/evidence.qcow2"

        # Check if vmdk_file exists
        if not os.path.exists(qcow2_file):
            return JsonResponse({'error': f'QCOW2 file {qcow2_file} not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            change_qcow2(qcow2_file, folders)

            return JsonResponse({'message': f'Folders {", ".join(folders)} created successfully in {qcow2_file}'}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': f'Error executing guestfish: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    """This class-based view handles the POST request to create specified folders in a qcow2 disk image.

The method checks the validity and activity status of the provided API key. If the API key is invalid or
belongs to an inactive user, it returns an error message.

It then retrieves the list of folders and the UUID path from the request data. It uses the UUID path to form
the path to the qcow2 file.

It checks if the qcow2 file exists. If it doesn't, it returns an error.

It calls the change_qcow2 function to create the folders in the qcow2 file. If successful, it returns a success
message. If an error occurs, it returns an error message.

Attributes:
authentication_classes (list): A list of authentication classes to use for the view.
permission_classes (list): A list of permission classes to use for the view.

Methods:
post(request): Asynchronously handles the POST request."""

@method_decorator(csrf_exempt, name='dispatch')
class CreateSnapshotView(View):
    """
    API View that handles POST requests to create a snapshot of a specific VM.

    This view requires an API key for authentication. If the API key is valid and is associated
    with an active user, it calls the `create_snapshot` asynchronous function to create the snapshot.

    If the API key is missing, invalid, or associated with an inactive user, an error message is returned.

    The response indicates either the snapshot name or an error message in a JSON format:
    {
        "snapshot_name": <string>
    }
    or
    {
        "error": <string>
    }
    """
    async def post(self, request, uuid):
        """
        Handles the POST request to create a snapshot of a VM.

        Args:
            request: The HTTP request from the client. Expected to contain the API key in the headers.
            uuid: The UUID of the VM to create the snapshot.

        Returns:
            JsonResponse: A JsonResponse that either contains the snapshot name or an error message.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key:
            try:
                api_key = await sync_to_async(ApiKey.objects.get)(key=api_key)
                user = await sync_to_async(getattr)(api_key, 'user')
                if not user.is_active:
                    return JsonResponse({'error': 'User account is disabled.'}, status=401)
            except ApiKey.DoesNotExist:
                return JsonResponse({'error': 'Invalid API key'}, status=401)
        else:
            return JsonResponse({'error': 'API key required'}, status=401)

        snapshot_name = await create_snapshot(uuid)
        return JsonResponse({'snapshot_name': snapshot_name}, status=200)
    """API View that handles POST requests to create a snapshot of a specific VM.

This view requires an API key for authentication. If the API key is valid and is associated
with an active user, it calls the `create_snapshot` asynchronous function to create the snapshot.

If the API key is missing, invalid, or associated with an inactive user, an error message is returned.

The response indicates either the snapshot name or an error message in a JSON format:
{
    "snapshot_name": <string>
}
or
{
    "error": <string>
}"""

class CreateSshKeysView(APIView):
    """
    API endpoint that allows the creation of SSH keys by adding a public key to the authorized keys file of the forensic investigator user.

    This view accepts a POST request with a public key as a parameter. The public key is added to the authorized keys file of the forensic investigator user.
    An API key or session-based authentication is required.
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        """
        Adds a public key to the authorized keys file of the forensic investigator user.

        Args:
            request: The POST request received by the server.

        Returns:
            Response: A Django Response object containing the result of adding the public key to the authorized keys file.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key:
            try:
                api_key = ApiKey.objects.get(key=api_key)
                user = api_key.user
                if not user.is_active:
                    return Response({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return Response({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)

        # Read public key from request data
        public_key = request.data.get('public_key')
        if not public_key:
            return Response({'error': 'Missing public key parameter'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if public key already exists in authorized keys
        authorized_keys_file = f'/home/forensicinvestigator/.ssh/authorized_keys'
        with open(authorized_keys_file, 'r') as f:
            authorized_keys = f.read()

        if public_key in authorized_keys:
            return Response({'message': 'Public key already added to authorized keys'}, status=status.HTTP_200_OK)

        # Add public key to authorized keys of the forensicinvestigator user
        try:
            with open(authorized_keys_file, 'a') as f:
                f.write(public_key + '\n')
        except FileNotFoundError:
            return Response({'error': 'Failed to append public key to authorized keys file'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'Public key added to authorized keys'}, status=status.HTTP_200_OK)
    """API endpoint that allows the creation of SSH keys by adding a public key to the authorized keys file of the forensic investigator user.

This view accepts a POST request with a public key as a parameter. The public key is added to the authorized keys file of the forensic investigator user.
An API key or session-based authentication is required."""

@method_decorator(csrf_exempt, name='dispatch')
class DeleteISOFileView(View):
    """
    This is a Django view that provides an endpoint for deleting an ISO file from a specified directory.

    The DeleteISOFileView class handles HTTP POST requests to delete an ISO file identified by its filename.

    The class uses Django's View, which means it can handle different types of HTTP requests. It currently only
    implements handling of POST requests via the defined post() method.

    Attributes:
        authentication_classes (list): A list of authentication classes the view should use. It's empty in this case.
        permission_classes (list): A list of permissions the view should enforce. It's empty in this case.
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request, filename):
        """
        This method handles the POST request to delete an ISO file.

        It first validates the API key from the request. If the API key is valid and belongs to an active user,
        it checks if the ISO directory and the specified ISO file exist. If they do, it deletes the ISO file
        and returns a confirmation message.

        Parameters:
        request (HttpRequest): The request object that has triggered this method.
        filename (str): The name of the ISO file to be deleted.

        Returns:
        JsonResponse: A JSON object containing a confirmation message or an error message with an HTTP status code.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key:
            try:
                api_key = ApiKey.objects.get(key=api_key)
                user = api_key.user
                if not user.is_active:
                    return JsonResponse({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return JsonResponse({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)

        iso_dir = '/forensicVM/mnt/iso'
        if not os.path.exists(iso_dir):
            return JsonResponse({'error': 'ISO directory not found'}, status=status.HTTP_404_NOT_FOUND)

        iso_file_path = os.path.join(iso_dir, filename)
        if not os.path.isfile(iso_file_path):
            return JsonResponse({'error': f'ISO file {filename} not found'}, status=status.HTTP_404_NOT_FOUND)

        os.remove(iso_file_path)

        return JsonResponse({'message': f'ISO file {filename} deleted successfully'}, status=status.HTTP_200_OK)
    """This is a Django view that provides an endpoint for deleting an ISO file from a specified directory.

The DeleteISOFileView class handles HTTP POST requests to delete an ISO file identified by its filename.

The class uses Django's View, which means it can handle different types of HTTP requests. It currently only
implements handling of POST requests via the defined post() method.

Attributes:
    authentication_classes (list): A list of authentication classes the view should use. It's empty in this case.
    permission_classes (list): A list of permissions the view should enforce. It's empty in this case."""

@method_decorator(csrf_exempt, name='dispatch')
class DeleteSnapshotView(View):
    """
    API View that handles POST requests to delete a snapshot of a specific VM.

    This view requires an API key for authentication. If the API key is valid and is associated
    with an active user, it calls the `delete_snapshot` asynchronous function to delete the snapshot.

    If the API key is missing, invalid, or associated with an inactive user, or if the snapshot
    name is missing in the request data, an error message is returned.

    The response indicates either a success or an error message in a JSON format:
    {
        "message": <string>
    }
    or
    {
        "error": <string>
    }
    """
    async def post(self, request, uuid):
        """
        Handles the POST request to delete a snapshot of a VM.

        Args:
            request: The HTTP request from the client. Expected to contain the API key in the headers,
                     and the snapshot name in the request data.
            uuid: The UUID of the VM whose snapshot is to be deleted.

        Returns:
            JsonResponse: A JsonResponse that either contains a success message or an error message.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key:
            try:
                api_key = await sync_to_async(ApiKey.objects.get)(key=api_key)
                user = await sync_to_async(getattr)(api_key, 'user')
                if not user.is_active:
                    return JsonResponse({'error': 'User account is disabled.'}, status=401)
            except ApiKey.DoesNotExist:
                return JsonResponse({'error': 'Invalid API key'}, status=401)
        else:
            return JsonResponse({'error': 'API key required'}, status=401)

        snapshot_name = request.POST.get('snapshot_name')
        if not snapshot_name:
            return JsonResponse({'error': 'Snapshot name required'}, status=400)

        delete_status = await delete_snapshot(uuid, snapshot_name)
        return JsonResponse({'message': delete_status}, status=200)
    """API View that handles POST requests to delete a snapshot of a specific VM.

This view requires an API key for authentication. If the API key is valid and is associated
with an active user, it calls the `delete_snapshot` asynchronous function to delete the snapshot.

If the API key is missing, invalid, or associated with an inactive user, or if the snapshot
name is missing in the request data, an error message is returned.

The response indicates either a success or an error message in a JSON format:
{
    "message": <string>
}
or
{
    "error": <string>
}"""

class DeleteVMView(APIView):
    """
    This Django View handles POST requests to delete a VM. It authenticates the request and then removes the specified VM's
    directory from the filesystem.

    The VM is identified by its UUID, which should be included in the URL of the request.
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request, uuid):
        """
        This method handles the POST request to delete a VM. It checks for user authentication, verifies the
        existence of the VM, and then deletes the VM's directory.

        Args:
            request (django.http.HttpRequest): The request instance.
            uuid (str): The UUID of the VM to be deleted.

        Returns:
            rest_framework.response.Response: A JSON response with the result of the operation.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key:
            try:
                api_key = ApiKey.objects.get(key=api_key)
                user = api_key.user
                if not user.is_active:
                    return Response({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return Response({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)

        vm_path = f"/forensicVM/mnt/vm/{uuid}"
        if not os.path.exists(vm_path):
            return Response({'error': f'Path for UUID {uuid} not found'}, status=status.HTTP_404_NOT_FOUND)

        # Delete the VM directory
        try:
            shutil.rmtree(vm_path)
            result = {'vm_deleted': True}
        except Exception as e:
            result = {'vm_deleted': False, 'error': str(e)}

        return Response(result, status=status.HTTP_200_OK)
    """This Django View handles POST requests to delete a VM. It authenticates the request and then removes the specified VM's
directory from the filesystem.

The VM is identified by its UUID, which should be included in the URL of the request."""

@method_decorator(csrf_exempt, name='dispatch')
class DownloadEvidenceView(View):
    """
    This class-based view handles the GET request to download a VMDK evidence file related to a specific VM.

    The method checks the validity and activity status of the provided API key. If the API key is invalid or
    belongs to an inactive user, it returns an error message.

    It uses the UUID from the URL parameters to form the path to the VM directory and checks if it exists.

    It then forms the path to the qcow2 file and converts it to a VMDK file using qemu-img. If this process fails,
    it returns an error message.

    It checks if the VMDK evidence file exists. If it doesn't, it returns an error.

    Finally, it returns the evidence file as a FileResponse, allowing the client to download it.

    Attributes:
    authentication_classes (list): A list of authentication classes to use for the view.
    permission_classes (list): A list of permission classes to use for the view.

    Methods:
    get(request, uuid): Asynchronously handles the GET request.
    """
    authentication_classes = []
    permission_classes = []

    async def get(self, request, uuid):
        """
        Asynchronously handles the GET request to download a VMDK evidence file.

        Parameters:
        request (HttpRequest): The request object that has triggered this method.
        uuid (str): The UUID of the VM.

        Returns:
        FileResponse: A FileResponse object containing the VMDK evidence file,
                      or a JsonResponse object containing an error message.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key:
            try:
                api_key = await sync_to_async(ApiKey.objects.get)(key=api_key)
                user = await sync_to_async(getattr)(api_key, 'user')
                if not user.is_active:
                    return JsonResponse({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return JsonResponse({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)

        vm_path = f"/forensicVM/mnt/vm/{uuid}"
        vm_exists = os.path.exists(vm_path)

        if not vm_exists:
            return JsonResponse({'error': f'VM with UUID {uuid} not found'}, status=status.HTTP_404_NOT_FOUND)

        evidence_path = f"/forensicVM/mnt/vm/{uuid}/evidence.vmdk"
        qcow2_path = f"/forensicVM/mnt/vm/{uuid}/evidence.qcow2"
        cmd = f"qemu-img convert {qcow2_path} -f qcow2 -O vmdk {evidence_path}"
        try:
            subprocess.run(cmd, shell=True, check=True)
            result = {'folder_mounted': True}
        except subprocess.CalledProcessError as e:
            return Response({'error': f"Error converting evidence disk: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        evidence_exists = os.path.exists(evidence_path)

        if not evidence_exists:
            return JsonResponse({'error': f'Evidence file not found for VM with UUID {uuid}'}, status=status.HTTP_404_NOT_FOUND)

        # Return the evidence file as a FileResponse
        response = FileResponse(open(evidence_path, 'rb'), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(evidence_path)}"'
        return response
    """This class-based view handles the GET request to download a VMDK evidence file related to a specific VM.

The method checks the validity and activity status of the provided API key. If the API key is invalid or
belongs to an inactive user, it returns an error message.

It uses the UUID from the URL parameters to form the path to the VM directory and checks if it exists.

It then forms the path to the qcow2 file and converts it to a VMDK file using qemu-img. If this process fails,
it returns an error message.

It checks if the VMDK evidence file exists. If it doesn't, it returns an error.

Finally, it returns the evidence file as a FileResponse, allowing the client to download it.

Attributes:
authentication_classes (list): A list of authentication classes to use for the view.
permission_classes (list): A list of permission classes to use for the view.

Methods:
get(request, uuid): Asynchronously handles the GET request."""

@method_decorator(csrf_exempt, name='dispatch')
class DownloadNetworkPcapView(View):
    """
    View to download the pcap files of a VM.

    The view has no authentication or permission restrictions.
    The get method is used to handle the downloading of pcap files of a VM with a given UUID.
    """
    authentication_classes = []
    permission_classes = []

    async def get(self, request, uuid):
        """
        Handle a GET request to download the pcap files of a VM.

        This method first checks if there is an API key error.
        If there's an API key error, it returns a JSON response with the error.
        The method then checks if the VM with the provided UUID exists.
        If the VM does not exist, it returns a JSON response indicating the error.
        It creates a zip file of all pcap files associated with the VM.
        If successful, the method returns a FileResponse with the created zip file.

        Parameters:
        ----------
        request : django.http.HttpRequest
            The request instance for the current request.
        uuid : str
            The UUID of the VM.

        Returns:
        -------
        django.http.FileResponse
            A FileResponse with the zip file of the pcap files of the VM.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key:
            try:
                api_key = await sync_to_async(ApiKey.objects.get)(key=api_key)
                user = await sync_to_async(getattr)(api_key, 'user')
                if not user.is_active:
                    return JsonResponse({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return JsonResponse({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)

        vm_path = f"/forensicVM/mnt/vm/{uuid}"
        vm_exists = os.path.exists(vm_path)

        if not vm_exists:
            return JsonResponse({'error': f'VM with UUID {uuid} not found'}, status=status.HTTP_404_NOT_FOUND)

        pcap_path = f"/forensicVM/mnt/vm/{uuid}/pcap/"

        # Create a zip file containing all pcap files
        zip_file_path = f"/forensicVM/mnt/vm/{uuid}/pcap.zip"
        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            for pcap_file in glob.glob(f"{pcap_path}/*.pcap"):
                zipf.write(pcap_file, os.path.basename(pcap_file))

        # Return the zip file as a FileResponse
        response = FileResponse(open(zip_file_path, 'rb'), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(zip_file_path)}"'
        return response
    """View to download the pcap files of a VM.

The view has no authentication or permission restrictions.
The get method is used to handle the downloading of pcap files of a VM with a given UUID."""

@method_decorator(csrf_exempt, name='dispatch')
class DownloadScreenshotsView(View):
    """
    This is an API view for downloading all the screenshots of a Virtual Machine (VM) as a ZIP file.
    It requires the UUID of the VM to be specified as a path parameter in the URL.

    Authentication is done via an API key which must be included in the request headers.

    This view will attempt to collect all the screenshots of the VM, convert them to JPG format if necessary,
    compress them into a ZIP file, and then return it as a file download.
    """
    authentication_classes = []
    permission_classes = []

    async def get(self, request, uuid):
        """
        Handle the GET request to the DownloadScreenshotsView.

        The function will first authenticate the user using the API key provided in the headers.
        If the user is authenticated, it will proceed to collect all the screenshots of the VM specified by
        the UUID in the URL, convert them to JPG format, compress them into a ZIP file, and then return the
        ZIP file as a response.

        Args:
            request: The HTTP request.
            uuid: The UUID of the VM to download the screenshots from.

        Returns:
            A FileResponse with the ZIP file containing all screenshots. If an error occurs, a JsonResponse
            with an error message will be returned.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key:
            try:
                api_key = await sync_to_async(ApiKey.objects.get)(key=api_key)
                user = await sync_to_async(getattr)(api_key, 'user')
                if not user.is_active:
                    return JsonResponse({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return JsonResponse({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)

        vm_path = f"/forensicVM/mnt/vm/{uuid}"
        vm_exists = os.path.exists(vm_path)

        if not vm_exists:
            return JsonResponse({'error': f'VM with UUID {uuid} not found'}, status=status.HTTP_404_NOT_FOUND)

        screenshots_path = f"/forensicVM/mnt/vm/{uuid}/screenshots/"

        # Convert PNG files to JPG
        for png_file in glob.glob(f"{screenshots_path}/*.png"):
            jpg_file = os.path.splitext(png_file)[0] + ".jpg"
            img = Image.open(png_file)
            img.convert("RGB").save(jpg_file)

        # Create a zip file containing all JPG files
        zip_file_path = f"/forensicVM/mnt/vm/{uuid}/screenshots.zip"
        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            for jpg_file in glob.glob(f"{screenshots_path}/*.jpg"):
                zipf.write(jpg_file, os.path.basename(jpg_file))

        # Return the zip file as a FileResponse
        response = FileResponse(open(zip_file_path, 'rb'), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(zip_file_path)}"'
        return response
    """This is an API view for downloading all the screenshots of a Virtual Machine (VM) as a ZIP file.
It requires the UUID of the VM to be specified as a path parameter in the URL.

Authentication is done via an API key which must be included in the request headers.

This view will attempt to collect all the screenshots of the VM, convert them to JPG format if necessary,
compress them into a ZIP file, and then return it as a file download."""

class DownloadVideoView(APIView):
    """
    A Django APIView class for downloading a video file.

    This class uses SessionAuthentication for user authentication.
    It doesn't implement any specific permission classes.

    Attributes:
    ----------
    authentication_classes : list
        List of authentication classes the view uses. Here, it's SessionAuthentication.
    permission_classes : list
        List of permission classes the view uses. Here, it's an empty list.

    Methods:
    -------
    get(request, uuid, filename):
        Returns a FileResponse to download a video file.
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = []

    def get(self, request, uuid, filename):
        """
        Handles GET request to download a video.

        This method checks if the user is authenticated, validates the filename,
        constructs the file path, checks if the file exists, and returns a FileResponse
        for the client to download the video.

        Parameters:
        ----------
        request : django.http.HttpRequest
            The request instance for the current request.
        uuid : str
            The unique identifier for the video file's directory.
        filename : str
            The name of the video file to download.

        Returns:
        -------
        django.http.FileResponse
            A FileResponse that initiates the video file download.

        Raises:
        ------
        Http404
            If the video file does not exist.
        """
        user, api_key_error = self.get_user_or_key_error(request)
        if api_key_error:
            return api_key_error

        # Check filename to prevent directory traversal attacks
        if not re.match('^[a-zA-Z0-9_.-]*$', filename):
            return JsonResponse({'error': 'Invalid filename'}, status=status.HTTP_400_BAD_REQUEST)

        video_dir = f"/forensicVM/mnt/vm/{uuid}/video"
        filepath = join(video_dir, filename)

        if not isfile(filepath):
            raise Http404("Video does not exist")

        video_file = open(filepath, 'rb')
        response = FileResponse(video_file)
        #response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{urlquote(basename(filepath))}'
        response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{quote(basename(filepath))}'
        return response

    def get_user_or_key_error(self, request):
        """
        Retrieves the authenticated user from the request or returns an API key error.

        This method attempts to get an authenticated user from the request.
        If the user is authenticated, it will return the user and None for the error.
        If the user is not authenticated, it will attempt to authenticate the user using an API key provided in the request.
        If the API key is valid and associated with an active user, it returns the user and None for the error.
        If the API key is invalid or the user associated with the key is not active, it returns None for the user and a JsonResponse indicating the error.
        If no API key is provided in the request, it returns None for the user and a JsonResponse indicating that an API key is required.

        Parameters:
        ----------
        request : django.http.HttpRequest
            The request instance for the current request.

        Returns:
        -------
        tuple
            A tuple where the first element is the authenticated user or None if no user could be authenticated,
            and the second element is None or a JsonResponse containing an error message.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            print("DEBUG: USER AUTHENTICATED")
        elif api_key:
            try:
                api_key = ApiKey.objects.get(key=api_key)
                user = getattr(api_key, 'user')
                if not user.is_active:
                    return None, JsonResponse({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return None, JsonResponse({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return None, JsonResponse({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)
        return user, None
    """A Django APIView class for downloading a video file.

This class uses SessionAuthentication for user authentication.
It doesn't implement any specific permission classes.

Attributes:
----------
authentication_classes : list
    List of authentication classes the view uses. Here, it's SessionAuthentication.
permission_classes : list
    List of permission classes the view uses. Here, it's an empty list.

Methods:
-------
get(request, uuid, filename):
    Returns a FileResponse to download a video file."""

@method_decorator(csrf_exempt, name='dispatch')
class EjectCDROMView(View):
    """
    This is a Django view that provides an endpoint for ejecting the CD-ROM from a virtual machine.

    The EjectCDROMView class handles HTTP GET requests to eject the CD-ROM from a virtual machine
    identified by its unique identifier (uuid).

    The class uses Django's View, which means it can handle different types of HTTP requests. It currently only
    implements handling of GET requests via the defined get() method. It also supports authentication via sessions.

    Attributes:
        authentication_classes (list): A list of authentication classes the view should use.
                                       It includes SessionAuthentication.
        permission_classes (list): A list of permissions the view should enforce. Empty in this case.
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = []

    async def get(self, request, uuid):
        """
        This method handles the GET request to eject the CD-ROM from a virtual machine.

        It first validates the user or API key from the request. If the user is authenticated or the API key is valid,
        it calls the asynchronous function eject_cdrom() to eject the CD-ROM and returns a confirmation message.

        Parameters:
        request (HttpRequest): The request object that has triggered this method.
        uuid (str): The unique identifier of the virtual machine.

        Returns:
        JsonResponse: A JSON object containing a confirmation message or an error message with an HTTP status code.
        """
        user, api_key_error = await sync_to_async(self.get_user_or_key_error)(request)
        if api_key_error:
            return api_key_error

        cdrom_status = await eject_cdrom(uuid)
        return JsonResponse({'message': cdrom_status}, status=status.HTTP_200_OK)

    def get_user_or_key_error(self, request):
        """
        This method handles the user authentication and API key validation.

        It checks if the user is authenticated. If not, it validates the API key from the request. If the API key
        is invalid or belongs to an inactive user, it returns a JSON response with an error message.

        Parameters:
        request (HttpRequest): The request object that has triggered this method.

        Returns:
        tuple: A tuple containing the user (if authenticated or API key is valid) and a JSON response (if any error occurs).
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            print("DEBUG: USER AUTHENTICATED")
        elif api_key:
            try:
                api_key = ApiKey.objects.get(key=api_key)
                user = getattr(api_key, 'user')
                if not user.is_active:
                    return None, JsonResponse({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return None, JsonResponse({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return None, JsonResponse({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)
        return user, None
    """This is a Django view that provides an endpoint for ejecting the CD-ROM from a virtual machine.

The EjectCDROMView class handles HTTP GET requests to eject the CD-ROM from a virtual machine
identified by its unique identifier (uuid).

The class uses Django's View, which means it can handle different types of HTTP requests. It currently only
implements handling of GET requests via the defined get() method. It also supports authentication via sessions.

Attributes:
    authentication_classes (list): A list of authentication classes the view should use.
                                   It includes SessionAuthentication.
    permission_classes (list): A list of permissions the view should enforce. Empty in this case."""

class ForensicImageVMStatus(APIView):
    """
    API endpoint that allows retrieval of the status of a forensic image VM via GET requests.

    This view accepts a GET request with a UUID and returns the status of the corresponding forensic image VM.
    If the VM path or mode file cannot be found, it returns a 404 Not Found error.
    An API key or session-based authentication is required.
    """
    authentication_classes = [SessionAuthentication]                # ADDED
    #authentication_classes = []
    permission_classes = []

    def get(self, request, uuid):
        """
        Retrieves the status of the forensic image VM specified by the UUID.

        Args:
            request: The GET request received by the server.
            uuid: The UUID of the forensic image VM.

        Returns:
            Response: A Django Response object containing the VM status and related information.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        user = getattr(request, 'user', None)                       # IF sync
        #user = await sync_to_async(getattr)(request, 'user', None)  # ASYNC: Get the user in the request
        if user and user.is_authenticated:                          # User is authenticated via session
            print("DEBUG: USER AUTHENTICATED")
            pass                                                    # Add this extra block to the request
        elif api_key:                                               # <--- Changed
            try:
                api_key = ApiKey.objects.get(key=api_key)
                user = api_key.user
                if not user.is_active:
                    return Response({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return Response({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)

        vm_path = f"/forensicVM/mnt/vm/{uuid}"
        run_path = os.path.join(vm_path, "run")
        pid_file = os.path.join(run_path, "run.pid")
        mode_file = os.path.join(run_path, "mode")

        #if not os.path.exists(mode_file):
        if not os.path.exists(vm_path):
            print("Does no exist")
            return Response({'PATH': 'not_exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            result = {'PATH': 'exists'}

            if os.path.exists(pid_file):
                with open(pid_file, 'r') as f:
                    pid = f.read().strip()

                cmd = f"ps -ef | grep {pid} | grep {uuid}"
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                output, _ = process.communicate()

                if output:
                    result['vm_status'] = 'running'

                    mode = None
                    if os.path.exists(mode_file):
                        with open(mode_file, 'r') as f:
                            mode = f.read().strip()
                    result['running_mode'] = mode

                    qemu_cmd = output.decode("utf-8").strip()
                    vnc_port = re.search(r'-display vnc=0.0.0.0:(\d+)', qemu_cmd)
                    websocket_port = re.search(r',websocket=(\d+)', qemu_cmd)
                    qmp_file = re.search(r'-qmp unix:([^,]+)', qemu_cmd)

                    if vnc_port:
                        result['vnc_port'] = int(vnc_port.group(1))
                    else:
                        result['vm_status'] = 'stopped'
                    if websocket_port:
                        result['websocket_port'] = int(websocket_port.group(1))
                    else:
                        result['vm_status'] = 'stopped'
                    if qmp_file:
                        result['qmp_file'] = qmp_file.group(1)
                    else:
                        result['vm_status'] = 'stopped'
                else:
                    result['vm_status'] = 'stopped'
            else:
                result['vm_status'] = 'stopped'

            return Response(result, status=status.HTTP_200_OK)
    """API endpoint that allows retrieval of the status of a forensic image VM via GET requests.

This view accepts a GET request with a UUID and returns the status of the corresponding forensic image VM.
If the VM path or mode file cannot be found, it returns a 404 Not Found error.
An API key or session-based authentication is required."""

@method_decorator(csrf_exempt, name='dispatch')
class GetAvailableMemoryView(View):
    """
    API View that handles GET requests to retrieve available system memory.

    This view requires an API key for authentication. If the API key is valid
    and is associated with an active user, the system's available memory is returned.
    The available memory is calculated using the get_available_memory function.

    If the API key is missing, invalid, or associated with an inactive user, an error message is returned.

    The available memory is returned in a JSON format:
    {
        "available_memory": <float>
    }
    """
    def get(self, request):
        """
        Handles the GET request to retrieve the system's available memory.

        Args:
            request: The HTTP request from the client. Expected to contain the API key in the headers.

        Returns:
            JsonResponse: A JsonResponse that either contains the available memory or an error message.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key:
            try:
                api_key = ApiKey.objects.get(key=api_key)
                user = api_key.user
                if not user.is_active:
                    return JsonResponse({'error': 'User account is disabled.'}, status=401)
            except ApiKey.DoesNotExist:
                return JsonResponse({'error': 'Invalid API key'}, status=401)
        else:
            return JsonResponse({'error': 'API key required'}, status=401)

        available_memory = get_available_memory()

        return JsonResponse({'available_memory': available_memory}, status=200)
    """API View that handles GET requests to retrieve available system memory.

This view requires an API key for authentication. If the API key is valid
and is associated with an active user, the system's available memory is returned.
The available memory is calculated using the get_available_memory function.

If the API key is missing, invalid, or associated with an inactive user, an error message is returned.

The available memory is returned in a JSON format:
{
    "available_memory": <float>
}"""

@method_decorator(csrf_exempt, name='dispatch')
class InsertCDROMView(View):
    """
    This is a Django view that provides an endpoint for inserting a CD-ROM into a virtual machine.

    The InsertCDROMView class handles HTTP GET requests to insert a CD-ROM into a virtual machine
    identified by its unique identifier (uuid) and the filename of the ISO image.

    The class uses Django's View, which means it can handle different types of HTTP requests. It currently only
    implements handling of GET requests via the defined get() method. It also supports authentication via sessions.

    Attributes:
        authentication_classes (list): A list of authentication classes the view should use.
                                       It includes SessionAuthentication.
        permission_classes (list): A list of permissions the view should enforce. Empty in this case.
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = []

    async def get(self, request, uuid, filename):
        """
        This method handles the GET request to insert a CD-ROM into a virtual machine.

        It first validates the user or API key from the request. If the user is authenticated or the API key is valid,
        it calls the asynchronous function insert_cdrom() to insert the CD-ROM and returns a confirmation message.

        Parameters:
        request (HttpRequest): The request object that has triggered this method.
        uuid (str): The unique identifier of the virtual machine.
        filename (str): The filename of the ISO image to insert into the CD-ROM drive.

        Returns:
        JsonResponse: A JSON object containing a confirmation message or an error message with an HTTP status code.
        """
        user, api_key_error = await sync_to_async(self.get_user_or_key_error)(request)
        if api_key_error:
            return api_key_error

        cdrom_status = await insert_cdrom(uuid, filename)
        return JsonResponse({'message': cdrom_status}, status=status.HTTP_200_OK)

    def get_user_or_key_error(self, request):
        """
        This method handles the user authentication and API key validation.

        It checks if the user is authenticated. If not, it validates the API key from the request. If the API key
        is invalid or belongs to an inactive user, it returns a JSON response with an error message.

        Parameters:
        request (HttpRequest): The request object that has triggered this method.

        Returns:
        tuple: A tuple containing the user (if authenticated or API key is valid) and a JSON response (if any error occurs).
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            print("DEBUG: USER AUTHENTICATED")
        elif api_key:
            try:
                api_key = ApiKey.objects.get(key=api_key)
                user = getattr(api_key, 'user')
                if not user.is_active:
                    return None, JsonResponse({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return None, JsonResponse({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return None, JsonResponse({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)
        return user, None
    """This is a Django view that provides an endpoint for inserting a CD-ROM into a virtual machine.

The InsertCDROMView class handles HTTP GET requests to insert a CD-ROM into a virtual machine
identified by its unique identifier (uuid) and the filename of the ISO image.

The class uses Django's View, which means it can handle different types of HTTP requests. It currently only
implements handling of GET requests via the defined get() method. It also supports authentication via sessions.

Attributes:
    authentication_classes (list): A list of authentication classes the view should use.
                                   It includes SessionAuthentication.
    permission_classes (list): A list of permissions the view should enforce. Empty in this case."""

@method_decorator(csrf_exempt, name='dispatch')
class InsertNetworkCardView(View):
    """
    This is a Django view that provides an endpoint for inserting a network card into a virtual machine.

    The InsertNetworkCardView class handles HTTP GET requests to insert a network card into a virtual machine
    identified by its unique identifier (uuid). The class uses Django's View, which means it can handle different types
    of HTTP requests. It currently only implements handling of GET requests via the defined get() method.

    Attributes:
        authentication_classes (list): A list of authentication classes the view should use. Empty in this case.
        permission_classes (list): A list of permissions the view should enforce. Empty in this case.
    """
    authentication_classes = []
    permission_classes = []

    async def get(self, request, uuid):
        """
        This method handles the GET request to insert a network card into a virtual machine.

        It first validates the API key from the request. If the key is valid, it calls the asynchronous function
        insert_network_card() to insert the network card and returns a confirmation message.

        Parameters:
        request (HttpRequest): The request object that has triggered this method.
        uuid (str): The unique identifier of the virtual machine.

        Returns:
        JsonResponse: A JSON object containing a confirmation message or an error message with an HTTP status code.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key:
            try:
                #api_key = ApiKey.objects.get(key=api_key)
                api_key = await sync_to_async(ApiKey.objects.get)(key=api_key)
                user = await sync_to_async(getattr)(api_key, 'user')
                if not user.is_active:
                    print('User account disabled')
                    return JsonResponse({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                print('Invalid key')
                return JsonResponse({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            print('api required')
            return JsonResponse({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)

        if not uuid:
            print('uuid required')
            return JsonResponse({'error': 'UUID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            print('inserting network card')
            await insert_network_card(uuid)
            print('inserted')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return JsonResponse({'message': 'Network card inserted.'}, status=status.HTTP_200_OK)
    """This is a Django view that provides an endpoint for inserting a network card into a virtual machine.

The InsertNetworkCardView class handles HTTP GET requests to insert a network card into a virtual machine
identified by its unique identifier (uuid). The class uses Django's View, which means it can handle different types
of HTTP requests. It currently only implements handling of GET requests via the defined get() method.

Attributes:
    authentication_classes (list): A list of authentication classes the view should use. Empty in this case.
    permission_classes (list): A list of permissions the view should enforce. Empty in this case."""

class ListISOFilesView(APIView):
    """
    This is a Django view that provides an endpoint for retrieving a list of all ISO files in a specified directory.

    The ListISOFilesView class handles HTTP GET requests to retrieve the ISO files.

    The class uses Django's APIView, which allows it to handle different types of HTTP requests. It currently only
    implements handling of GET requests via the defined get() method.

    Attributes:
        authentication_classes (list): A list of authentication classes the view should use. It's empty in this case.
        permission_classes (list): A list of permissions the view should enforce. It's empty in this case.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        """
        This method handles the GET request to list all ISO files.

        It first validates the API key from the request. If the API key is valid and belongs to an active user,
        it checks if the ISO directory exists and retrieves a list of all ISO files in the directory. If the directory
        does not exist, it returns an error message.

        Parameters:
        request (HttpRequest): The request object that has triggered this method.

        Returns:
        JsonResponse: A JSON object containing a list of all ISO files in the directory or an error message with an HTTP status code.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key:
            try:
                api_key = ApiKey.objects.get(key=api_key)
                user = api_key.user
                if not user.is_active:
                    return JsonResponse({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return JsonResponse({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)

        iso_dir = '/forensicVM/mnt/iso'
        if not os.path.exists(iso_dir):
            return JsonResponse({'error': 'ISO directory not found'}, status=status.HTTP_404_NOT_FOUND)

        iso_files = []
        for file in os.listdir(iso_dir):
            if file.endswith('.iso'):
                iso_files.append(file)
        return JsonResponse({'iso_files': iso_files}, status=status.HTTP_200_OK)
    """This is a Django view that provides an endpoint for retrieving a list of all ISO files in a specified directory.

The ListISOFilesView class handles HTTP GET requests to retrieve the ISO files.

The class uses Django's APIView, which allows it to handle different types of HTTP requests. It currently only
implements handling of GET requests via the defined get() method.

Attributes:
    authentication_classes (list): A list of authentication classes the view should use. It's empty in this case.
    permission_classes (list): A list of permissions the view should enforce. It's empty in this case."""

class ListPluginsView(APIView):
    """
    This is a Django REST Framework view that extends from the APIView base class.

    The ListPluginsView class defines behavior for handling HTTP GET requests on the URL path associated with it.
    The purpose of this class is to provide an endpoint that responds with a list of available forensic plugins.
    The view uses Django's APIView, which means it can handle different types of HTTP requests.
    It currently only implements handling of GET requests via the defined get() method.

    Attributes:
        authentication_classes (list): A list of authentication classes the view should use. Empty in this case.
        permission_classes (list): A list of permissions the view should enforce. Empty in this case.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        """
        Handles GET requests to list all available forensic plugins.

        The method retrieves the API key from the request headers and validates it. If the API key is invalid or
        belongs to an inactive user, an error response is returned.

        The method then reads the 'plugins' directory and looks for 'run.sh' files in each of the subdirectories.
        For each such file found, it gets the plugin information by calling the get_plugin_info() function.

        If the 'plugins' directory does not exist, an error response is returned.

        Parameters:
        request (HttpRequest): The request object that has triggered this method.

        Returns:
        JsonResponse: A JSON object containing a list of all available plugins with their names, descriptions and directories.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key:
            try:
                api_key = ApiKey.objects.get(key=api_key)
                user = api_key.user
                if not user.is_active:
                    return JsonResponse({'error': 'User account is disabled.'}, status=401)
            except ApiKey.DoesNotExist:
                return JsonResponse({'error': 'Invalid API key'}, status=401)
        else:
            return JsonResponse({'error': 'API key required'}, status=401)

        plugins_dir = '/forensicVM/plugins'
        if not os.path.exists(plugins_dir):
            return JsonResponse({'error': 'Plugins directory not found'}, status=404)

        plugin_files = []
        for root, dirs, files in os.walk(plugins_dir):
            for file in files:
                if file == 'run.sh':
                    plugin_dir = os.path.basename(os.path.dirname(os.path.join(root, file)))
                    plugin_files.append({
                        'plugin_name': get_plugin_info(plugin_dir, 'plugin_name'),
                        'plugin_description': get_plugin_info(plugin_dir, 'plugin_description'),
                        'plugin_dir': plugin_dir
                    })

        return JsonResponse({'plugins': plugin_files}, status=200)
    """This is a Django REST Framework view that extends from the APIView base class.

The ListPluginsView class defines behavior for handling HTTP GET requests on the URL path associated with it.
The purpose of this class is to provide an endpoint that responds with a list of available forensic plugins.
The view uses Django's APIView, which means it can handle different types of HTTP requests.
It currently only implements handling of GET requests via the defined get() method.

Attributes:
    authentication_classes (list): A list of authentication classes the view should use. Empty in this case.
    permission_classes (list): A list of permissions the view should enforce. Empty in this case."""

class ListVideosView(APIView):
    """
    A Django APIView class for listing all the .mp4 video files in a specific directory.

    This class uses SessionAuthentication for user authentication.
    It doesn't implement any specific permission classes.

    Attributes:
    ----------
    authentication_classes : list
        List of authentication classes the view uses. Here, it's SessionAuthentication.
    permission_classes : list
        List of permission classes the view uses. Here, it's an empty list.

    Methods:
    -------
    get(request, uuid):
        Returns a JsonResponse with a list of all .mp4 video files in the specified directory.
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = []

    def get(self, request, uuid):
        """
        Handles GET request to list all .mp4 video files in a specific directory.

        This method checks if the user is authenticated, constructs the video directory path,
        checks if the directory exists, and returns a JsonResponse containing a list of all .mp4 video files
        in the directory, sorted in ascending order.

        Parameters:
        ----------
        request : django.http.HttpRequest
            The request instance for the current request.
        uuid : str
            The unique identifier for the video files' directory.

        Returns:
        -------
        django.http.JsonResponse
            A JsonResponse containing a list of all .mp4 video files in the specified directory.
        """
        user, api_key_error = self.get_user_or_key_error(request)
        if api_key_error:
            return api_key_error

        video_dir = f"/forensicVM/mnt/vm/{uuid}/video"
        #video_exists = os.path.exists(video_dir)

        if not os.path.exists(video_dir):
            return JsonResponse({'error': 'Video directory not found'}, status=status.HTTP_404_NOT_FOUND)

        video_files = []
        for file in os.listdir(video_dir):
            if file.endswith('.mp4'):
                video_files.append(file)
            video_files.sort(reverse=True)
        return JsonResponse({'video_files': video_files}, status=status.HTTP_200_OK)

    def get_user_or_key_error(self, request):
        """
        Retrieves the authenticated user from the request or returns an API key error.

        This method attempts to get an authenticated user from the request.
        If the user is authenticated, it will return the user and None for the error.
        If the user is not authenticated, it will attempt to authenticate the user using an API key provided in the request.
        If the API key is valid and associated with an active user, it returns the user and None for the error.
        If the API key is invalid or the user associated with the key is not active, it returns None for the user and a JsonResponse indicating the error.
        If no API key is provided in the request, it returns None for the user and a JsonResponse indicating that an API key is required.

        Parameters:
        ----------
        request : django.http.HttpRequest
            The request instance for the current request.

        Returns:
        -------
        tuple
            A tuple where the first element is the authenticated user or None if no user could be authenticated,
            and the second element is None or a JsonResponse containing an error message.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            print("DEBUG: USER AUTHENTICATED")
        elif api_key:
            try:
                api_key = ApiKey.objects.get(key=api_key)
                user = getattr(api_key, 'user')
                if not user.is_active:
                    return None, JsonResponse({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return None, JsonResponse({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return None, JsonResponse({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)
        return user, None
    """A Django APIView class for listing all the .mp4 video files in a specific directory.

This class uses SessionAuthentication for user authentication.
It doesn't implement any specific permission classes.

Attributes:
----------
authentication_classes : list
    List of authentication classes the view uses. Here, it's SessionAuthentication.
permission_classes : list
    List of permission classes the view uses. Here, it's an empty list.

Methods:
-------
get(request, uuid):
    Returns a JsonResponse with a list of all .mp4 video files in the specified directory."""

class MemorySizeView(View):
    """
    API View that handles GET requests to fetch the current memory size of a Virtual Machine (VM).

    This view requires an API key for authentication. If the API key is valid and is associated
    with an active user, the memory size is retrieved from the script files in the VM directory.

    If the API key is missing, invalid, or associated with an inactive user, or if the memory size
    cannot be found, an error message is returned.

    The response indicates either the memory size or an error message in a JSON format:
    {
        "memory_size": <int>
    }
    or
    {
        "error": <string>
    }
    """
    def get(self, request, uuid):
        """
        Handles the GET request to fetch the memory size of a VM.

        Args:
            request: The HTTP request from the client. Expected to contain the API key in the headers.
            uuid: The UUID of the VM whose memory size is to be fetched.

        Returns:
            JsonResponse: A JsonResponse that either contains the memory size or an error message.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key:
            try:
                api_key = ApiKey.objects.get(key=api_key)
                user = api_key.user
                if not user.is_active:
                    return JsonResponse({'error': 'User account is disabled.'}, status=401)
            except ApiKey.DoesNotExist:
                return JsonResponse({'error': 'Invalid API key'}, status=401)
        else:
            return JsonResponse({'error': 'API key required'}, status=401)

        vm_path = f"/forensicVM/mnt/vm/{uuid}"
        if not os.path.exists(vm_path):
            return JsonResponse({'error': f'Path for UUID {uuid} not found'}, status=404)

        script_files = glob.glob(os.path.join(vm_path, '*.sh'))
        if not script_files:
            return JsonResponse({'error': f'No script files found for UUID {uuid}'}, status=404)

        recent_script_file = max(script_files, key=os.path.getctime)

        with open(recent_script_file, 'r') as f:
            script_content = f.read()

        memory_pattern = r'-m\s+(\d+)'
        memory_match = re.search(memory_pattern, script_content)

        if memory_match:
            memory_size = int(memory_match.group(1))
            return JsonResponse({'memory_size': memory_size}, status=200)
        else:
            return JsonResponse({'error': 'Memory parameter not found in the script.'}, status=404)
    """API View that handles GET requests to fetch the current memory size of a Virtual Machine (VM).

This view requires an API key for authentication. If the API key is valid and is associated
with an active user, the memory size is retrieved from the script files in the VM directory.

If the API key is missing, invalid, or associated with an inactive user, or if the memory size
cannot be found, an error message is returned.

The response indicates either the memory size or an error message in a JSON format:
{
    "memory_size": <int>
}
or
{
    "error": <string>
}"""

@method_decorator(csrf_exempt, name='dispatch')
class MemorySnapshotView(View):
    """
    This is an API view for creating a memory snapshot of a Virtual Machine (VM) and downloading it.
    It requires the UUID of the VM to be specified as a path parameter in the URL.

    Authentication is done via an API key which must be included in the request headers.

    This view will attempt to create a memory snapshot of the VM and then return it as a file download.
    """
    authentication_classes = []
    permission_classes = []

    async def get(self, request, uuid):
        """
        Handle the GET request to the MemorySnapshotView.

        The function will first authenticate the user using the API key provided in the headers.
        If the user is authenticated, it will proceed to create a memory snapshot of the VM
        specified by the UUID in the URL and then return the snapshot file as a response.

        Args:
            request: The HTTP request.
            uuid: The UUID of the VM to create a memory snapshot of.

        Returns:
            A FileResponse with the memory snapshot file. If an error occurs, a JsonResponse
            with an error message will be returned.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key:
            try:
                api_key = await sync_to_async(ApiKey.objects.get)(key=api_key)
                user = await sync_to_async(getattr)(api_key, 'user')
                if not user.is_active:
                    return JsonResponse({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return JsonResponse({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)

        snapshot_file = await memory_snapshot(uuid)
        response = FileResponse(open(snapshot_file, 'rb'), content_type='application/octet-stream', as_attachment=True, filename=os.path.basename(snapshot_file))
        return response
    """This is an API view for creating a memory snapshot of a Virtual Machine (VM) and downloading it.
It requires the UUID of the VM to be specified as a path parameter in the URL.

Authentication is done via an API key which must be included in the request headers.

This view will attempt to create a memory snapshot of the VM and then return it as a file download."""

class MountFolderView(APIView):
    """
    This Django View handles POST requests to mount a folder in a VM. It authenticates the request and then executes
    a mount command to bind the specified folder to a location within the VM's filesystem.

    The VM is identified by its UUID, which should be included in the URL of the request.

    The folder to be mounted should be specified in the request's JSON body using the 'folder' key.
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request, uuid):
        """
        This method handles the POST request to mount a folder in a VM. It checks for user authentication, verifies the
        input folder path, and then sends the mount command.

        Args:
            request (django.http.HttpRequest): The request instance.
            uuid (str): The UUID of the VM where the folder is to be mounted.

        Returns:
            rest_framework.response.Response: A JSON response with the result of the operation.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key:
            try:
                api_key = ApiKey.objects.get(key=api_key)
                user = api_key.user
                if not user.is_active:
                    return Response({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return Response({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)

        folder_to_mount = request.data.get('folder')
        if not folder_to_mount:
            return Response({'error': 'No folder specified to mount'}, status=status.HTTP_400_BAD_REQUEST)

        mount_path = f"/forensicVM/mnt/vm/{uuid}/mnt"
        os.makedirs(mount_path, exist_ok=True)

        cmd = f"mount --bind {folder_to_mount} {mount_path}"
        try:
            subprocess.run(cmd, shell=True, check=True)
            result = {'folder_mounted': True}
            return Response(result, status=status.HTTP_200_OK)
        except subprocess.CalledProcessError as e:
            return Response({'error': f"Error mounting folder: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    """This Django View handles POST requests to mount a folder in a VM. It authenticates the request and then executes
a mount command to bind the specified folder to a location within the VM's filesystem.

The VM is identified by its UUID, which should be included in the URL of the request.

The folder to be mounted should be specified in the request's JSON body using the 'folder' key."""

class ProtectedView(APIView):
    """
    API endpoint that creates a protected view requiring an API key for access.

    This view accepts a GET request and checks for the presence of an API key in the request headers.
    If a valid API key is found, the access is granted and a success message is returned.
    An API key is required for accessing this view.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        """
        Handles the GET request and checks for the presence of a valid API key.

        Args:
            request: The GET request received by the server.

        Returns:
            Response: A Django Response object indicating the result of the access check.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key:
            try:
                api_key = ApiKey.objects.get(key=api_key)
                user = api_key.user
                if not user.is_active:
                    return Response({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return Response({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'message': 'Access granted'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)
    """API endpoint that creates a protected view requiring an API key for access.

This view accepts a GET request and checks for the presence of an API key in the request headers.
If a valid API key is found, the access is granted and a success message is returned.
An API key is required for accessing this view."""

@method_decorator(csrf_exempt, name='dispatch')
class RecordVideoVMView(View):
    """
    A Django View class that handles the video recording process of a virtual machine.

    This class implements the POST HTTP method to start and manage the recording of a video.
    If the requested virtual machine (identified by uuid) exists and is not already recording,
    it starts a new recording, creating a video file in a specified directory.
    The recording runs asynchronously for a maximum duration of three hours or until it is manually stopped.

    If the virtual machine is already recording, the POST request will return an error.
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = []

    async def post(self, request, uuid):
        """
        Asynchronously handle a POST request to start recording a video.

        This method attempts to start a recording for the specified virtual machine.
        It checks if the machine exists and if a recording is not already in progress.
        If these conditions are met, it sets up a new video file and starts the recording.
        The recording runs for a maximum duration of three hours or until it is manually stopped.
        After the recording is finished, it cleans up the resources and sends a response indicating success.

        Parameters:
        ----------
        request : django.http.HttpRequest
            The request instance for the current request.
        uuid : str
            The unique identifier for the virtual machine.

        Returns:
        -------
        JsonResponse
            A JsonResponse indicating whether the recording started successfully or detailing any errors that occurred.

        Raises:
        ------
        Exception
            Any exception that occurs while starting or managing the recording.
        """
        user, api_key_error = await sync_to_async(self.get_user_or_key_error)(request)
        if api_key_error:
            return api_key_error

        vm_path = f"/forensicVM/mnt/vm/{uuid}"
        vm_exists = await sync_to_async(os.path.exists)(vm_path)

        if not vm_exists:
            return JsonResponse({'error': f'VM with UUID {uuid} not found'}, status=404)

        video_path = f"/forensicVM/mnt/vm/{uuid}/video/"
        if not os.path.exists(video_path):
            os.makedirs(video_path)  # Recreate the empty directory

        video_count = len(os.listdir(video_path))
        output_video_path = os.path.join(video_path, f"video{video_count + 1:04d}.mp4")

        video_writer = None  # Start with no video writer

        try:
            record = False
            if uuid not in recordings:
                record = True
                print("uuid not in the recordigs")
            elif uuid in recordings and not recordings[uuid]:
                record = True
                print("uuid is in the recordings, but not in the uuid")


            if record:
            #if uuid not in recordings:
                recordings[uuid] = True
                scheduler = AsyncIOScheduler()
                scheduler.add_job(create_video, 'interval', seconds=0.04, id=f'create_video_job_{uuid}', args=[uuid, output_video_path], replace_existing=True)

                #scheduler.add_job(create_video, 'interval', seconds=0.04, id=f'create_video_job_{uuid}', args=[uuid, output_video_path, video_writer], replace_existing=True)
                scheduler.start()

                for _ in range(3600*3):  # run the loop for 3600 interactions*3 (three hour)
                    await asyncio.sleep(1)  # sleep for 1 second
                    if not recordings[uuid]:  # if recordings[uuid] is False, break the loop
                        break

                scheduler.remove_job(f'create_video_job_{uuid}')
                if uuid in video_writers:
                    video_writers[uuid].release()
                    del video_writers[uuid]  # remove the VideoWriter from the dictionary


                result = {'video_recorded': True, 'message': f'Video recorded with the name video{video_count + 1:04d}.mp4'}
                recordings[uuid] = False
                return JsonResponse(result, status=status.HTTP_200_OK)

                #return JsonResponse({"status": "Recording stopped"}, status=200)
            else:
                return JsonResponse({"error": "Recording already in progress"}, status=400)
        except Exception as e:
            print(e)


    def get_user_or_key_error(self, request):
        """
        Check if the user is authenticated or if there is an API key error.

        This method checks if the user associated with the request is authenticated.
        If the user is not authenticated, it checks if there's an API key in the request.
        If the API key is valid and associated with an active user, the method returns this user.
        If the API key is not valid or the user is not active, it returns a JSON response with the corresponding error.
        If there's no API key at all, it returns a JSON response indicating that the API key is required.

        Parameters:
        ----------
        request : django.http.HttpRequest
            The request instance for the current request.

        Returns:
        -------
        tuple
            A tuple where the first element is the authenticated user or None,
            and the second element is a JsonResponse with an error message or None.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            print("DEBUG: USER AUTHENTICATED")
        elif api_key:
            try:
                api_key = ApiKey.objects.get(key=api_key)
                user = getattr(api_key, 'user')
                if not user.is_active:
                    return None, JsonResponse({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return None, JsonResponse({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return None, JsonResponse({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)
        return user, None
    """A Django View class that handles the video recording process of a virtual machine.

This class implements the POST HTTP method to start and manage the recording of a video.
If the requested virtual machine (identified by uuid) exists and is not already recording,
it starts a new recording, creating a video file in a specified directory.
The recording runs asynchronously for a maximum duration of three hours or until it is manually stopped.

If the virtual machine is already recording, the POST request will return an error."""

@method_decorator(csrf_exempt, name='dispatch')
class RecreateFoldersView(View):
    """
    This Django view handles POST requests to recreate a set of folders inside a QCOW2 file in a Virtual Machine.

    The view first authenticates the request based on the provided API key. If the user related to the API key is not active,
    it returns an error.

    Upon successful authentication, the view retrieves a list of folders and a VM uuid from the request. It then creates
    a new QCOW2 file in the corresponding VM directory and formats it with NTFS filesystem, followed by creating the specified
    folders in the root directory of the filesystem. If the QCOW2 file already exists, it is first deleted.

    If the QCOW2 file is created and formatted successfully, the view returns a success message. If an error occurs during
    the operation, it returns an error message.

    The view uses the `create_and_format_qcow2` function to perform the creation and formatting operations.
    """
    authentication_classes = []
    permission_classes = []

    async def post(self, request):
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key:
            try:
                api_key = await sync_to_async(ApiKey.objects.get)(key=api_key)
                user = await sync_to_async(getattr)(api_key, 'user')
                if not user.is_active:
                    return JsonResponse({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return JsonResponse({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)

        # Get the list of folders from the POST data
        folders = request.POST.getlist('folders')
        uuid_path = request.POST.get('uuid_path')
        qcow2_file = f"/forensicVM/mnt/vm/{uuid_path}/evidence.qcow2"

        try:
            # Remove existing qcow2_file if it exists
            if os.path.exists(qcow2_file):
                os.remove(qcow2_file)

            # Create and format the Qcow2 file
            print("before create qcow2")
            create_and_format_qcow2(qcow2_file, folders)
            print("after create qcow2")

            return JsonResponse({'message': f'Folders {", ".join(folders)} created successfully in {qcow2_file}'}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': f'Error executing guestfish: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    """This Django view handles POST requests to recreate a set of folders inside a QCOW2 file in a Virtual Machine.

The view first authenticates the request based on the provided API key. If the user related to the API key is not active,
it returns an error.

Upon successful authentication, the view retrieves a list of folders and a VM uuid from the request. It then creates
a new QCOW2 file in the corresponding VM directory and formats it with NTFS filesystem, followed by creating the specified
folders in the root directory of the filesystem. If the QCOW2 file already exists, it is first deleted.

If the QCOW2 file is created and formatted successfully, the view returns a success message. If an error occurs during
the operation, it returns an error message.

The view uses the `create_and_format_qcow2` function to perform the creation and formatting operations."""

@method_decorator(csrf_exempt, name='dispatch')
class RemoveVMDateTimeView(View):
    """
    View to remove the datetime line from a VM's configuration.

    The view has no authentication or permission restrictions.
    The post method is used to handle the removal of the datetime line from the configuration of a VM with a given UUID.
    """
    authentication_classes = []
    permission_classes = []

    async def post(self, request):
        """
        Handle a POST request to remove the datetime line from a VM's configuration.

        This method first checks if the user is authenticated or if there is an API key error.
        If there's an API key error, it returns a JSON response with the error.
        The method then retrieves the UUID from the POST data.
        It locates the .vnc configuration file for the VM with the provided UUID, reads its content, and removes any line containing the '-rtc base=' string.
        If successful, the method returns a JSON response indicating the successful operation.
        If there's an error, it returns a JSON response with the error message.

        Parameters:
        ----------
        request : django.http.HttpRequest
            The request instance for the current request.

        Returns:
        -------
        django.http.JsonResponse
            A JsonResponse indicating the result of the operation.
        """
        api_key = request.META.get('HTTP_X_API_KEY')

        user = await sync_to_async(getattr)(request, 'user', None)  # Get the user in the request
        if user and user.is_authenticated:                          # User is authenticated via session
            pass                                                    # Add this extra block to the request
        elif api_key:                                               # <--- Changed
            try:
                api_key = await sync_to_async(ApiKey.objects.get)(key=api_key)
                user = await sync_to_async(getattr)(api_key, 'user')
                if not user.is_active:
                    return JsonResponse({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return JsonResponse({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)

        # Get the UUID from the POST data
        uuid = request.POST.get('uuid')

        try:
            # Get the .vnc file path
            vnc_file_path = glob.glob(f"/forensicVM/mnt/vm/{uuid}/*vnc.sh")[0]

            # Read the content of the file
            with open(vnc_file_path, 'r') as file:
                lines = file.readlines()

            # Remove the -rtc base=<datetime> line if it exists
            lines = [line for line in lines if '-rtc base=' not in line]

            # Write the changes back to the file
            with open(vnc_file_path, 'w') as file:
                file.writelines(lines)

            return JsonResponse({'message': f'Date time line removed successfully for VM {uuid}'}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': f'Error updating VM date time: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    """View to remove the datetime line from a VM's configuration.

The view has no authentication or permission restrictions.
The post method is used to handle the removal of the datetime line from the configuration of a VM with a given UUID."""

@method_decorator(csrf_exempt, name='dispatch')
class ResetVMView(View):
    """
    This Django View handles POST requests to reset a VM. It authenticates the request and then uses the
    `system_reset` function to send a reset command to the VM.

    The VM is identified by its UUID, which should be included in the URL of the request.
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = []

    async def post(self, request, uuid):
        """
        This method handles the POST request to reset a VM. It checks for user authentication, verifies the
        existence of the VM, and then sends the reset command.

        Args:
            request (django.http.HttpRequest): The request instance.
            uuid (str): The UUID of the VM to be reset.

        Returns:
            django.http.JsonResponse: A JSON response with the result of the operation.
        """
        user, api_key_error = await sync_to_async(self.get_user_or_key_error)(request)
        if api_key_error:
            return api_key_error

        vm_path = f"/forensicVM/mnt/vm/{uuid}"
        vm_exists = await sync_to_async(os.path.exists)(vm_path)

        if not vm_exists:
            return JsonResponse({'error': f'VM with UUID {uuid} not found'}, status=status.HTTP_404_NOT_FOUND)

        await system_reset(uuid)

        result = {'vm_reset': True, 'message': f'Reset command sent to VM with UUID {uuid}'}

        return JsonResponse(result, status=status.HTTP_200_OK)

    def get_user_or_key_error(self, request):
        """
        Helper method to retrieve the authenticated user from the request, or return an error response if
        the request is not authenticated.

        The request can be authenticated either through session-based authentication or by including an
        'X-API-KEY' header in the request.

        Args:
            request: The Django request object.

        Returns:
            If the request is authenticated, returns a tuple where the first element is the authenticated user
            and the second element is None.

            If the request is not authenticated, returns a tuple where the first element is None and the second
            element is a JsonResponse with an error message.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            print("DEBUG: USER AUTHENTICATED")
        elif api_key:
            try:
                api_key = ApiKey.objects.get(key=api_key)
                user = getattr(api_key, 'user')
                if not user.is_active:
                    return None, JsonResponse({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return None, JsonResponse({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return None, JsonResponse({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)
        return user, None
    """This Django View handles POST requests to reset a VM. It authenticates the request and then uses the
`system_reset` function to send a reset command to the VM.

The VM is identified by its UUID, which should be included in the URL of the request."""

@method_decorator(csrf_exempt, name='dispatch')
class RollbackSnapshotView(View):
    """
    API View that handles POST requests to rollback a snapshot of a specific VM.

    This view requires an API key for authentication. If the API key is valid and is associated
    with an active user, it calls the `rollback_snapshot` asynchronous function to rollback to the snapshot.

    If the API key is missing, invalid, or associated with an inactive user, or if the snapshot
    name is missing in the request data, an error message is returned.

    The response indicates either a success or an error message in a JSON format:
    {
        "message": <string>
    }
    or
    {
        "error": <string>
    }
    """
    async def post(self, request, uuid):
        """
        Handles the POST request to rollback to a snapshot of a VM.

        Args:
            request: The HTTP request from the client. Expected to contain the API key in the headers,
                     and the snapshot name in the request data.
            uuid: The UUID of the VM to rollback the snapshot.

        Returns:
            JsonResponse: A JsonResponse that either contains a success message or an error message.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key:
            try:
                api_key = await sync_to_async(ApiKey.objects.get)(key=api_key)
                user = await sync_to_async(getattr)(api_key, 'user')
                if not user.is_active:
                    return JsonResponse({'error': 'User account is disabled.'}, status=401)
            except ApiKey.DoesNotExist:
                return JsonResponse({'error': 'Invalid API key'}, status=401)
        else:
            return JsonResponse({'error': 'API key required'}, status=401)

        snapshot_name = request.POST.get('snapshot_name')
        if not snapshot_name:
            return JsonResponse({'error': 'Snapshot name required'}, status=400)

        rollback_status = await rollback_snapshot(uuid, snapshot_name)
        return JsonResponse({'message': rollback_status}, status=200)
    """API View that handles POST requests to rollback a snapshot of a specific VM.

This view requires an API key for authentication. If the API key is valid and is associated
with an active user, it calls the `rollback_snapshot` asynchronous function to rollback to the snapshot.

If the API key is missing, invalid, or associated with an inactive user, or if the snapshot
name is missing in the request data, an error message is returned.

The response indicates either a success or an error message in a JSON format:
{
    "message": <string>
}
or
{
    "error": <string>
}"""

class RunPluginView(APIView):
    """
    This Django view handles GET requests to run a forensic plugin script on a specified image within a Virtual Machine.

    The view first authenticates the request based on the provided API key. If the user related to the API key is not active,
    it returns an error.

    Upon successful authentication, the view retrieves the plugin directory and VM uuid from the request parameters.
    It validates the existence of the plugin script and the image, both identified using the provided parameters.

    If the validation is successful, it attempts to run the plugin script on the image and returns the script's stdout as
    the response. If the script fails to run, the error details are returned in the response.

    If the validation fails because of the non-existence of the plugin script or the image, an appropriate error message is returned.

    This view does not require any special permissions or authentication classes, as it is intended to be used internally
    by the system.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        """
        Handles GET requests to execute a specific forensic plugin on a VM image.

        The method retrieves the API key from the request headers and validates it. If the API key is invalid or
        belongs to an inactive user, an error response is returned.

        The method retrieves the plugin directory and image UUID from the GET parameters. It validates these parameters
        by checking the existence of the plugin script and the image path. If any of these does not exist, an error response is returned.

        The method looks for the latest '.qcow2-sda' file within the image path and sets it as the target for the plugin.

        Upon successful validation, the method attempts to run the plugin script on the image using a bash subprocess. The output
        from the subprocess is returned in the response.

        If the plugin script execution fails, the error details are returned in the response.

        Parameters:
        request (HttpRequest): The request object that has triggered this method.

        Returns:
        JsonResponse: A JSON object containing either the output of the plugin execution or an error message.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key:
            try:
                api_key = ApiKey.objects.get(key=api_key)
                user = api_key.user
                if not user.is_active:
                    return JsonResponse({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return JsonResponse({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)

        plugin_directory = request.GET.get('plugin_directory')
        image_uuid = request.GET.get('image_uuid')

        if not plugin_directory or not image_uuid:
            return JsonResponse({'error': 'Missing plugin_directory or image_uuid'}, status=status.HTTP_400_BAD_REQUEST)

        plugin_script_path = f'/forensicVM/plugins/{plugin_directory}/run.sh'
        image_path = f'/forensicVM/mnt/vm/{image_uuid}'

        if not os.path.exists(plugin_script_path):
            return JsonResponse({'error': 'Plugin script not found'}, status=status.HTTP_404_NOT_FOUND)

        if not os.path.exists(image_path):
            return JsonResponse({'error': 'Image path not found'}, status=status.HTTP_404_NOT_FOUND)

        file_list = os.listdir(image_path)
        file_list.sort(reverse=True)
        for file in file_list:
            if file.endswith('.qcow2-sda'):
                image_file = os.path.join(image_path, file)
                break
        else:
            return JsonResponse({'error': 'Image file not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            result = subprocess.run(['bash', plugin_script_path, 'run', image_file], capture_output=True, text=True)
            output = result.stdout.strip()
            return JsonResponse({'output': output}, status=status.HTTP_200_OK)
        except subprocess.CalledProcessError as e:
            return JsonResponse({'error': f'Plugin execution failed: {e.stderr}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    """This Django view handles GET requests to run a forensic plugin script on a specified image within a Virtual Machine.

The view first authenticates the request based on the provided API key. If the user related to the API key is not active,
it returns an error.

Upon successful authentication, the view retrieves the plugin directory and VM uuid from the request parameters.
It validates the existence of the plugin script and the image, both identified using the provided parameters.

If the validation is successful, it attempts to run the plugin script on the image and returns the script's stdout as
the response. If the script fails to run, the error details are returned in the response.

If the validation fails because of the non-existence of the plugin script or the image, an appropriate error message is returned.

This view does not require any special permissions or authentication classes, as it is intended to be used internally
by the system."""

class RunScriptView(APIView):
    """
    API endpoint for running a script.

    This view accepts a POST request and expects an API key to be provided in the request headers.
    The request should contain a 'script' parameter in the data payload, which contains the script to be executed.
    The script is executed using the subprocess module, and the output and error code are returned in the response.

    Note: This view does not perform any authentication or permission checks beyond validating the API key.
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        """
        Handles the POST request to execute a script.

        Args:
            request: The POST request received by the server.

        Returns:
            Response: A Django Response object containing the script output and error code.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key:
            try:
                api_key = ApiKey.objects.get(key=api_key)
            except ApiKey.DoesNotExist:
                return Response({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)

        if 'script' not in request.data:
            return Response({'error': 'Missing script parameter'}, status=status.HTTP_400_BAD_REQUEST)

        script = request.data['script']

        try:
            result = subprocess.run(script, shell=True, capture_output=True)
            return Response({'output': result.stdout.decode('utf-8'), 'error_code': result.returncode}, status=status.HTTP_200_OK)
        except subprocess.CalledProcessError as e:
            return Response({'error': e.output.decode('utf-8'), 'error_code': e.returncode}, status=status.HTTP_400_BAD_REQUEST)
    """API endpoint for running a script.

This view accepts a POST request and expects an API key to be provided in the request headers.
The request should contain a 'script' parameter in the data payload, which contains the script to be executed.
The script is executed using the subprocess module, and the output and error code are returned in the response.

Note: This view does not perform any authentication or permission checks beyond validating the API key."""

@method_decorator(csrf_exempt, name='dispatch')
class ScreenshotVMView(View):
    """
    A View class to handle the capture of screenshots from a Virtual Machine (VM).

    This View supports an asynchronous POST request, which initiates the capture of a screenshot from the VM.
    The VM is identified by its UUID, which is passed in the URL.

    Authentication is required to access this View. It supports both session-based authentication and API key
    authentication.

    """
    authentication_classes = [SessionAuthentication]                # ADDED
    permission_classes = []

    async def post(self, request, uuid):
        """
        Handles a POST request to capture a screenshot from a VM.

        The VM is identified by its UUID, which is passed in the URL.

        The request must be authenticated. This can be done either through session-based authentication or
        by including an 'X-API-KEY' header in the request.

        Args:
            request: The Django request object.
            uuid: The UUID of the VM.

        Returns:
            A JsonResponse containing the status of the screenshot operation. If the operation is successful,
            the response will include a 'screenshot_taken' key with a value of True, and a 'message' key with the
            screenshot number.

            If an error occurs, the JsonResponse will contain an 'error' key with a description of the error.
        """
        user, api_key_error = await sync_to_async(self.get_user_or_key_error)(request)
        if api_key_error:
            return api_key_error

        vm_path = f"/forensicVM/mnt/vm/{uuid}"
        vm_exists = await sync_to_async(os.path.exists)(vm_path)

        if not vm_exists:
            return JsonResponse({'error': f'VM with UUID {uuid} not found'}, status=status.HTTP_404_NOT_FOUND)

        screen_number = await screendump(uuid)

        result = {'screenshot_taken': True, 'message': f'{screen_number}'}

        return JsonResponse(result, status=status.HTTP_200_OK)


    def get_user_or_key_error(self, request):
        """
        Helper method to retrieve the authenticated user from the request, or return an error response if
        the request is not authenticated.

        The request can be authenticated either through session-based authentication or by including an
        'X-API-KEY' header in the request.

        Args:
            request: The Django request object.

        Returns:
            If the request is authenticated, returns a tuple where the first element is the authenticated user
            and the second element is None.

            If the request is not authenticated, returns a tuple where the first element is None and the second
            element is a JsonResponse with an error message.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            print("DEBUG: USER AUTHENTICATED")
        elif api_key:
            try:
                api_key = ApiKey.objects.get(key=api_key)
                user = getattr(api_key, 'user')
                if not user.is_active:
                    return None, JsonResponse({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return None, JsonResponse({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return None, JsonResponse({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)
        return user, None
    """A View class to handle the capture of screenshots from a Virtual Machine (VM).

This View supports an asynchronous POST request, which initiates the capture of a screenshot from the VM.
The VM is identified by its UUID, which is passed in the URL.

Authentication is required to access this View. It supports both session-based authentication and API key
authentication."""

@method_decorator(csrf_exempt, name='dispatch')
class ShutdownVMView(View):
    """
    This Django View handles POST requests to shutdown a VM. It authenticates the request and then uses the
    `system_shutdown` function to send a shutdown command to the VM.

    The VM is identified by its UUID, which should be included in the URL of the request.
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = []

    async def post(self, request, uuid):
        """
        This method handles the POST request to shut down a VM. It checks for user authentication, verifies the
        existence of the VM, and then sends the shutdown command.

        Args:
            request (django.http.HttpRequest): The request instance.
            uuid (str): The UUID of the VM to be shutdown.

        Returns:
            django.http.JsonResponse: A JSON response with the result of the operation.
        """
        user, api_key_error = await sync_to_async(self.get_user_or_key_error)(request)
        if api_key_error:
            return api_key_error

        vm_path = f"/forensicVM/mnt/vm/{uuid}"
        vm_exists = await sync_to_async(os.path.exists)(vm_path)

        if not vm_exists:
            return JsonResponse({'error': f'VM with UUID {uuid} not found'}, status=status.HTTP_404_NOT_FOUND)

        await system_shutdown(uuid)

        result = {'vm_shutdown': True, 'message': f'Shutdown command sent to VM with UUID {uuid}'}

        return JsonResponse(result, status=status.HTTP_200_OK)

    def get_user_or_key_error(self, request):
        """
        Helper method to retrieve the authenticated user from the request, or return an error response if
        the request is not authenticated.

        The request can be authenticated either through session-based authentication or by including an
        'X-API-KEY' header in the request.

        Args:
            request: The Django request object.

        Returns:
            If the request is authenticated, returns a tuple where the first element is the authenticated user
            and the second element is None.

            If the request is not authenticated, returns a tuple where the first element is None and the second
            element is a JsonResponse with an error message.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            print("DEBUG: USER AUTHENTICATED")
        elif api_key:
            try:
                api_key = ApiKey.objects.get(key=api_key)
                user = getattr(api_key, 'user')
                if not user.is_active:
                    return None, JsonResponse({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return None, JsonResponse({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return None, JsonResponse({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)
        return user, None
    """This Django View handles POST requests to shutdown a VM. It authenticates the request and then uses the
`system_shutdown` function to send a shutdown command to the VM.

The VM is identified by its UUID, which should be included in the URL of the request."""

@method_decorator(csrf_exempt, name='dispatch')
class SnapshotListView(View):
    """
    API View that handles GET requests to retrieve the list of snapshots of a specific VM.

    This view requires an API key for authentication. If the API key is valid and is associated
    with an active user, it calls the `get_snapshots` asynchronous function to retrieve the list of snapshots.

    If the API key is missing, invalid, or associated with an inactive user, an error message is returned.

    The response includes a list of snapshots or an error message in a JSON format:
    {
        "snapshots": [<list of snapshots>]
    }
    or
    {
        "error": <string>
    }
    """
    async def get(self, request, uuid):
        """
        Handles the GET request to retrieve the list of snapshots of a VM.

        Args:
            request: The HTTP request from the client. Expected to contain the API key in the headers.
            uuid: The UUID of the VM to get the snapshots.

        Returns:
            JsonResponse: A JsonResponse that either contains the list of snapshots or an error message.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key:
            try:
                api_key = await sync_to_async(ApiKey.objects.get)(key=api_key)
                user = await sync_to_async(getattr)(api_key, 'user')
                if not user.is_active:
                    return JsonResponse({'error': 'User account is disabled.'}, status=401)
            except ApiKey.DoesNotExist:
                return JsonResponse({'error': 'Invalid API key'}, status=401)
        else:
            return JsonResponse({'error': 'API key required'}, status=401)

        snapshots = await get_snapshots(uuid)
        return JsonResponse({'snapshots': snapshots}, status=200)
    """API View that handles GET requests to retrieve the list of snapshots of a specific VM.

This view requires an API key for authentication. If the API key is valid and is associated
with an active user, it calls the `get_snapshots` asynchronous function to retrieve the list of snapshots.

If the API key is missing, invalid, or associated with an inactive user, an error message is returned.

The response includes a list of snapshots or an error message in a JSON format:
{
    "snapshots": [<list of snapshots>]
}
or
{
    "error": <string>
}"""

@method_decorator(csrf_exempt, name='dispatch')
class StartTapInterfaceView(View):
    """
    View to start the tap interface of a VM.

    The view authenticates the user with SessionAuthentication. The post method is used to handle the start request of
    the tap interface of a VM.
    """
    authentication_classes = [SessionAuthentication]                # ADDED
    permission_classes = []

    async def post(self, request):
        """
        Handle a POST request to start the tap interface of a VM.

        This method first checks if there is an API key error.
        If there's an API key error, it returns a JSON response with the error.
        The method then gets the UUID from the POST data and tries to start the tap interface.
        It executes shell commands to get the tap interface and starts it.
        If the tap interface starts successfully, the method returns a JSON response with a positive message.
        If there's an error while starting the tap interface, the method returns a JSON response with the error.

        Parameters:
        ----------
        request : django.http.HttpRequest
            The request instance for the current request.

        Returns:
        -------
        django.http.JsonResponse
            A JsonResponse with a message about the status of the tap interface start action.
        """
        # Authenticate user using API key
        api_key = request.META.get('HTTP_X_API_KEY')
        #user = getattr(request, 'user', None)                       # IF sync
        #user = await sync_to_async(getattr)(request, 'user', None)  # ASYNC: Get the user in the request
        user = await sync_to_async(get_user)(request)
        if user and user.is_authenticated:                          # User is authenticated via session
            print("DEBUG: USER AUTHENTICATED")
            pass                                                    # Add this extra block to the request
        elif api_key:                                               # <--- Changed
            try:
                api_key = await sync_to_async(ApiKey.objects.get)(key=api_key)
                user = await sync_to_async(getattr)(api_key, 'user')
                if not user.is_active:
                    return JsonResponse({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return JsonResponse({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)

        # Get the uuid from the POST data
        uuid = request.POST.get('uuid')

        if not uuid:
            print('no UUID sent')
            return JsonResponse({'error': 'UUID required'}, status=status.HTTP_400_BAD_REQUEST)

        # Execute the command to get the tap interface
        cmd = f"ps -ef | grep qemu | grep {uuid}"
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()

        if error:
            return JsonResponse({'error': f'Error finding QEMU process: {error}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        tap_interface = output.decode().split('-netdev tap,id=u1,ifname=')[1].split(',')[0]

        # Start the tap interface
        start_tap_cmd = f"ifconfig {tap_interface} up"
        start_tap_process = subprocess.Popen(start_tap_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        start_tap_output, start_tap_error = start_tap_process.communicate()

        if start_tap_error:
            return JsonResponse({'error': f'Error starting tap interface: {start_tap_error}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return JsonResponse({'message': f'Tap interface {tap_interface} started successfully'}, status=status.HTTP_200_OK)
    """View to start the tap interface of a VM.

The view authenticates the user with SessionAuthentication. The post method is used to handle the start request of
the tap interface of a VM."""

class StartVMView(APIView):
    """
    API endpoint that allows VMs to be started via POST requests.

    This view accepts a POST request with a UUID and attempts to start the corresponding VM.
    If successful, it returns a 200 OK response with a JSON body indicating the VM has been started and provides the VNC and WebSocket ports.
    If the VM path or VNC script cannot be found, it returns a 404 Not Found error.
    An API key or session-based authentication is required.
    """
    authentication_classes = [SessionAuthentication]                # ADDED
    permission_classes = []

    def post(self, request, uuid):
        """
        Starts the VM specified by the UUID.

        Args:
            request: The POST request received by the server.
            uuid: The UUID of the VM to be started.

        Returns:
            Response: A Django Response object.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        user = getattr(request, 'user', None)                       # IF sync
        #user = await sync_to_async(getattr)(request, 'user', None)  # ASYNC: Get the user in the request
        if user and user.is_authenticated:                          # User is authenticated via session
            print("DEBUG: USER AUTHENTICATED")
            pass                                                    # Add this extra block to the request
        elif api_key:                                               # <--- Changed
            try:
                api_key = ApiKey.objects.get(key=api_key)
                user = api_key.user
                if not user.is_active:
                    return Response({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return Response({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)

        vm_path = f"/forensicVM/mnt/vm/{uuid}"
        if not os.path.exists(vm_path):
            return Response({'error': f'Path for UUID {uuid} not found'}, status=status.HTTP_404_NOT_FOUND)

        vnc_scripts = glob.glob(os.path.join(vm_path, '*-vnc.sh'))
        if not vnc_scripts:
            return Response({'error': f'No VNC script found for UUID {uuid}'}, status=status.HTTP_404_NOT_FOUND)

        recent_vnc_script = max(vnc_scripts, key=os.path.getctime)

        vnc_port, websocket_port = find_available_port(5900)

        cmd = f"screen -d -m -S {uuid} bash {recent_vnc_script} {vnc_port} {websocket_port}"
        subprocess.run(cmd, shell=True, check=True, cwd=vm_path)

        time.sleep(3)

        run_path = os.path.join(vm_path, "run")
        pid_file = os.path.join(run_path, "run.pid")
        vm_running = os.path.exists(pid_file) and subprocess.run(f"ps -ef | grep {uuid}", shell=True, check=True).returncode == 0

        result = {
            'vm_running': vm_running,
            'vnc_port': vnc_port,
            'websocket_port': websocket_port
        }

        return Response(result, status=status.HTTP_200_OK)
    """API endpoint that allows VMs to be started via POST requests.

This view accepts a POST request with a UUID and attempts to start the corresponding VM.
If successful, it returns a 200 OK response with a JSON body indicating the VM has been started and provides the VNC and WebSocket ports.
If the VM path or VNC script cannot be found, it returns a 404 Not Found error.
An API key or session-based authentication is required."""

@method_decorator(csrf_exempt, name='dispatch')
class StopTapInterfaceView(View):
    """
    View to stop the tap interface of a VM.

    The view authenticates the user with SessionAuthentication. The post method is used to handle the stop request of
    the tap interface of a VM.
    """
    authentication_classes = [SessionAuthentication]                # ADDED
    permission_classes = []

    async def post(self, request):
        """
        Handle a POST request to stop the tap interface of a VM.

        This method first checks if there is an API key error.
        If there's an API key error, it returns a JSON response with the error.
        The method then gets the UUID from the POST data and tries to stop the tap interface.
        It executes shell commands to get the tap interface and stops it.
        If the tap interface stops successfully, the method returns a JSON response with a positive message.
        If there's an error while stopping the tap interface, the method returns a JSON response with the error.

        Parameters:
        ----------
        request : django.http.HttpRequest
            The request instance for the current request.

        Returns:
        -------
        django.http.JsonResponse
            A JsonResponse with a message about the status of the tap interface stop action.
        """
        # Authenticate user using API key
        api_key = request.META.get('HTTP_X_API_KEY')
        #user = getattr(request, 'user', None)                       # IF sync
        #user = await sync_to_async(getattr)(request, 'user', None)  # ASYNC: Get the user in the request
        user = await sync_to_async(get_user)(request)

        if user and user.is_authenticated:                          # User is authenticated via session
            print("DEBUG: USER AUTHENTICATED")
            pass                                                    # Add this extra block to the request
        elif api_key:                                               # <--- Changed
            try:
                api_key = await sync_to_async(ApiKey.objects.get)(key=api_key)
                user = await sync_to_async(getattr)(api_key, 'user')
                if not user.is_active:
                    return JsonResponse({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return JsonResponse({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)

        # Get the uuid from the POST data
        uuid = request.POST.get('uuid')

        if not uuid:
            print('no UUID sent')
            return JsonResponse({'error': 'UUID required'}, status=status.HTTP_400_BAD_REQUEST)

        # Execute the command to get the tap interface
        cmd = f"ps -ef | grep qemu | grep {uuid}"
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()

        if error:
            return JsonResponse({'error': f'Error finding QEMU process: {error}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        tap_interface = output.decode().split('-netdev tap,id=u1,ifname=')[1].split(',')[0]

        # Start the tap interface
        start_tap_cmd = f"ifconfig {tap_interface} down"
        start_tap_process = subprocess.Popen(start_tap_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        start_tap_output, start_tap_error = start_tap_process.communicate()

        if start_tap_error:
            return JsonResponse({'error': f'Error stopping tap interface: {start_tap_error}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return JsonResponse({'message': f'Tap interface {tap_interface} stopped successfully'}, status=status.HTTP_200_OK)
    """View to stop the tap interface of a VM.

The view authenticates the user with SessionAuthentication. The post method is used to handle the stop request of
the tap interface of a VM."""

class StopVMView(APIView):
    """
    API endpoint that allows VMs to be stopped via POST requests.

    This view accepts a POST request with a UUID and attempts to stop the corresponding screen session of the VM.
    If successful, it returns a 200 OK response with a JSON body indicating the VM has been stopped.
    If the screen session cannot be found, it returns a 404 Not Found error.
    An API key is required for authentication.
    """
    authentication_classes = [SessionAuthentication]                # ADDED
    permission_classes = []

    def post(self, request, uuid):
        """
        Stops the VM specified by the UUID.

        Args:
            request: The POST request received by the server.
            uuid: The UUID of the VM to be stopped.

        Returns:
            Response: A Django Response object.
        """
        # Authenticate user using API key
        api_key = request.META.get('HTTP_X_API_KEY')
        user = getattr(request, 'user', None)                       # IF sync
        #user = await sync_to_async(getattr)(request, 'user', None)  # ASYNC: Get the user in the request
        if user and user.is_authenticated:                          # User is authenticated via session
            print("DEBUG: USER AUTHENTICATED")
            pass                                                    # Add this extra block to the request
        elif api_key:                                               # <--- Changed
            try:
                api_key = ApiKey.objects.get(key=api_key)
                user = api_key.user
                if not user.is_active:
                    return Response({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return Response({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)

        # Stop the screen session
        cmd = f"screen -S {uuid} -X quit"

        try:
            subprocess.run(cmd, shell=True, check=True)
        except CalledProcessError:
            return Response({'error': f'No screen session found for UUID {uuid}'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the screen session was terminated
        screen_status = subprocess.run(f"screen -list | grep {uuid}", shell=True, capture_output=True).stdout.decode('utf-8')
        vm_stopped = uuid not in screen_status

        result = {'vm_stopped': vm_stopped}
        return Response(result, status=status.HTTP_200_OK)
    """API endpoint that allows VMs to be stopped via POST requests.

This view accepts a POST request with a UUID and attempts to stop the corresponding screen session of the VM.
If successful, it returns a 200 OK response with a JSON body indicating the VM has been stopped.
If the screen session cannot be found, it returns a 404 Not Found error.
An API key is required for authentication."""

@method_decorator(csrf_exempt, name='dispatch')
class StopVideoRecordingVMView(View):
    """
    View to handle the stoppage of video recording.

    The view uses session authentication and has no permission restrictions.
    The post method is used to handle the stoppage of the video recording for a VM with a given UUID.
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = []

    async def post(self, request, uuid):
        """
        Handle a POST request to stop video recording for a VM with a given UUID.

        This method first checks if the user is authenticated or if there is an API key error.
        If there's an API key error, it returns a JSON response with the error.
        If the UUID is present in the recordings, it stops the recording by setting the corresponding value to False.
        If the UUID is not present, it returns a HTTP 400 error.
        Finally, it returns a JSON response confirming the stoppage of the recording.

        Parameters:
        ----------
        request : django.http.HttpRequest
            The request instance for the current request.
        uuid : str
            The UUID of the VM for which the recording should be stopped.

        Returns:
        -------
        django.http.JsonResponse
            A JsonResponse indicating the result of the operation.
        """
        user, api_key_error = await sync_to_async(self.get_user_or_key_error)(request)
        if api_key_error:
            return api_key_error

        if uuid in recordings:
            print("DEBUG: Stop uuid in recordings")
            recordings[uuid] = False
        else:
            return HttpResponseBadRequest(f'No recording to stop for VM with UUID {uuid}')
            recordings[uuid] = False


        result = {'video_recording_stopped': True, 'message': f'Video recording stopped for VM with UUID {uuid}'}

        return JsonResponse(result, status=status.HTTP_200_OK)

    def get_user_or_key_error(self, request):
        """
        Check if the user is authenticated or if there is an API key error.

        This method checks if the user associated with the request is authenticated.
        If the user is not authenticated, it checks if there's an API key in the request.
        If the API key is valid and associated with an active user, the method returns this user.
        If the API key is not valid or the user is not active, it returns a JSON response with the corresponding error.
        If there's no API key at all, it returns a JSON response indicating that the API key is required.

        Parameters:
        ----------
        request : django.http.HttpRequest
            The request instance for the current request.

        Returns:
        -------
        tuple
            A tuple where the first element is the authenticated user or None,
            and the second element is a JsonResponse with an error message or None.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            print("DEBUG: USER AUTHENTICATED")
        elif api_key:
            try:
                api_key = ApiKey.objects.get(key=api_key)
                user = getattr(api_key, 'user')
                if not user.is_active:
                    return None, JsonResponse({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return None, JsonResponse({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return None, JsonResponse({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)
        return user, None
    """View to handle the stoppage of video recording.

The view uses session authentication and has no permission restrictions.
The post method is used to handle the stoppage of the video recording for a VM with a given UUID."""

@method_decorator(csrf_exempt, name='dispatch')
class UploadISOView(View):
    """
    This is a Django view that provides an endpoint for uploading an ISO file to a specified directory.

    The UploadISOView class handles HTTP POST requests to receive an ISO file and save it to the directory.

    The class uses Django's View, which means it can handle different types of HTTP requests. It currently only
    implements handling of POST requests via the defined post() method.

    Attributes:
        authentication_classes (list): A list of authentication classes the view should use. It's empty in this case.
        permission_classes (list): A list of permissions the view should enforce. It's empty in this case.
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        """
        This method handles the POST request to upload an ISO file.

        It first validates the API key from the request. If the API key is valid and belongs to an active user,
        it checks if an ISO file is provided in the request. If it is, it saves the ISO file
        to a specified directory and returns a confirmation message.

        Parameters:
        request (HttpRequest): The request object that has triggered this method.

        Returns:
        JsonResponse: A JSON object containing a confirmation message or an error message with an HTTP status code.
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key:
            try:
                api_key = ApiKey.objects.get(key=api_key)
                user = api_key.user
                if not user.is_active:
                    return JsonResponse({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
            except ApiKey.DoesNotExist:
                return JsonResponse({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)

        iso_file = request.FILES.get('iso_file')
        if not iso_file:
            return JsonResponse({'error': 'Missing ISO file'}, status=status.HTTP_400_BAD_REQUEST)

        # Save the ISO file to the target directory
        upload_dir = '/forensicVM/mnt/iso'
        iso_file_path = os.path.join(upload_dir, iso_file.name)
        with open(iso_file_path, 'wb') as f:
            for chunk in iso_file.chunks():
                f.write(chunk)

        return JsonResponse({'message': 'ISO file uploaded successfully'}, status=status.HTTP_200_OK)
    """This is a Django view that provides an endpoint for uploading an ISO file to a specified directory.

The UploadISOView class handles HTTP POST requests to receive an ISO file and save it to the directory.

The class uses Django's View, which means it can handle different types of HTTP requests. It currently only
implements handling of POST requests via the defined post() method.

Attributes:
    authentication_classes (list): A list of authentication classes the view should use. It's empty in this case.
    permission_classes (list): A list of permissions the view should enforce. It's empty in this case."""

class View:
    """
    Intentionally simple parent class for all views. Only implements
    dispatch-by-method and simple sanity checking.
    """

    http_method_names = [
        "get",
        "post",
        "put",
        "patch",
        "delete",
        "head",
        "options",
        "trace",
    ]

    def __init__(self, **kwargs):
        """
        Constructor. Called in the URLconf; can contain helpful extra
        keyword arguments, and other things.
        """
        # Go through keyword arguments, and either save their values to our
        # instance, or raise an error.
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classproperty
    def view_is_async(cls):
        handlers = [
            getattr(cls, method)
            for method in cls.http_method_names
            if (method != "options" and hasattr(cls, method))
        ]
        if not handlers:
            return False
        is_async = asyncio.iscoroutinefunction(handlers[0])
        if not all(asyncio.iscoroutinefunction(h) == is_async for h in handlers[1:]):
            raise ImproperlyConfigured(
                f"{cls.__qualname__} HTTP handlers must either be all sync or all "
                "async."
            )
        return is_async

    @classonlymethod
    def as_view(cls, **initkwargs):
        """Main entry point for a request-response process."""
        for key in initkwargs:
            if key in cls.http_method_names:
                raise TypeError(
                    "The method name %s is not accepted as a keyword argument "
                    "to %s()." % (key, cls.__name__)
                )
            if not hasattr(cls, key):
                raise TypeError(
                    "%s() received an invalid keyword %r. as_view "
                    "only accepts arguments that are already "
                    "attributes of the class." % (cls.__name__, key)
                )

        def view(request, *args, **kwargs):
            self = cls(**initkwargs)
            self.setup(request, *args, **kwargs)
            if not hasattr(self, "request"):
                raise AttributeError(
                    "%s instance has no 'request' attribute. Did you override "
                    "setup() and forget to call super()?" % cls.__name__
                )
            return self.dispatch(request, *args, **kwargs)

        view.view_class = cls
        view.view_initkwargs = initkwargs

        # __name__ and __qualname__ are intentionally left unchanged as
        # view_class should be used to robustly determine the name of the view
        # instead.
        view.__doc__ = cls.__doc__
        view.__module__ = cls.__module__
        view.__annotations__ = cls.dispatch.__annotations__
        # Copy possible attributes set by decorators, e.g. @csrf_exempt, from
        # the dispatch method.
        view.__dict__.update(cls.dispatch.__dict__)

        # Mark the callback if the view class is async.
        if cls.view_is_async:
            view._is_coroutine = asyncio.coroutines._is_coroutine

        return view

    def setup(self, request, *args, **kwargs):
        """Initialize attributes shared by all view methods."""
        if hasattr(self, "get") and not hasattr(self, "head"):
            self.head = self.get
        self.request = request
        self.args = args
        self.kwargs = kwargs

    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if request.method.lower() in self.http_method_names:
            handler = getattr(
                self, request.method.lower(), self.http_method_not_allowed
            )
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def http_method_not_allowed(self, request, *args, **kwargs):
        logger.warning(
            "Method Not Allowed (%s): %s",
            request.method,
            request.path,
            extra={"status_code": 405, "request": request},
        )
        response = HttpResponseNotAllowed(self._allowed_methods())

        if self.view_is_async:

            async def func():
                return response

            return func()
        else:
            return response

    def options(self, request, *args, **kwargs):
        """Handle responding to requests for the OPTIONS HTTP verb."""
        response = HttpResponse()
        response.headers["Allow"] = ", ".join(self._allowed_methods())
        response.headers["Content-Length"] = "0"

        if self.view_is_async:

            async def func():
                return response

            return func()
        else:
            return response

    def _allowed_methods(self):
        return [m.upper() for m in self.http_method_names if hasattr(self, m)]
    """Intentionally simple parent class for all views. Only implements
dispatch-by-method and simple sanity checking."""

