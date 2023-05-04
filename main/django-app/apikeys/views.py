import os
import re
import subprocess
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ApiKey

class ForensicImageVMStatus(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, uuid):
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
        run_path = os.path.join(vm_path, "run")
        pid_file = os.path.join(run_path, "run.pid")
        mode_file = os.path.join(run_path, "mode")

        if not os.path.exists(vm_path):
            return Response({'PATH': 'does not exist'}, status=status.HTTP_404_NOT_FOUND)
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
                    if websocket_port:
                        result['websocket_port'] = int(websocket_port.group(1))
                    if qmp_file:
                        result['qmp_file'] = qmp_file.group(1)

                else:
                    result['vm_status'] = 'not running'
            else:
                result['vm_status'] = 'not running'

            return Response(result, status=status.HTTP_200_OK)

class CreateSshKeysView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
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


class ProtectedView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
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



class RunScriptView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
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
