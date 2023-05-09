import os
import re
import subprocess
import socket
import glob
import time
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ApiKey
from subprocess import CalledProcessError
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ApiKey
import os
import shutil
import asyncio
from asgiref.sync import async_to_sync
from asgiref.sync import sync_to_async
from qemu.qmp import QMPClient

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

async def system_shutdown(uuid):
    qmp = QMPClient('forensicVM')
    socket_path = f"/forensicVM/mnt/vm/{uuid}/run/qmp.sock"
    try:
        await qmp.connect(socket_path)
        res = await qmp.execute('query-status')
        print(f"VM status: {res['status']}")
    except Exception as e:
        print(e)

    res = await qmp.execute('system_powerdown')
    print(res)

    await qmp.disconnect()

@method_decorator(csrf_exempt, name='dispatch')
class ShutdownVMView(View):
    authentication_classes = []
    permission_classes = []

    async def post(self, request, uuid):
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

        await system_shutdown(uuid)

        result = {'vm_shutdown': True, 'message': f'Shutdown command sent to VM with UUID {uuid}'}

        return JsonResponse(result, status=status.HTTP_200_OK)



async def system_reset(uuid):
    qmp = QMPClient('forensicVM')
    socket_path = f"/forensicVM/mnt/vm/{uuid}/run/qmp.sock"
    try:
        await qmp.connect(socket_path)
        res = await qmp.execute('query-status')
        print(f"VM status: {res['status']}")
        status = {res['status']}
    except Exception as e:
        print(e)
    res = await qmp.execute('system_reset')
    print(res)
    if status == {'suspended'}:
        res = await qmp.execute('quit')
        print(res)
    await qmp.disconnect()

@method_decorator(csrf_exempt, name='dispatch')
class ResetVMView(View):
    authentication_classes = []
    permission_classes = []

    async def post(self, request, uuid):
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key:
            try:
                api_key = await sync_to_async(ApiKey.objects.get)(key=api_key)
                user = await sync_to_async(getattr)(api_key, 'user')
                #user = api_key.user
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

        await system_reset(uuid)

        result = {'vm_reset': True, 'message': f'Reset command sent to VM with UUID {uuid}'}

        return JsonResponse(result, status=status.HTTP_200_OK)

class MountFolderView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, uuid):
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

class DeleteVMView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, uuid):
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

class CheckVMExistsView(APIView):
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
        vm_exists = os.path.exists(vm_path)

        result = {'vm_exists': vm_exists}

        return Response(result, status=status.HTTP_200_OK)

def find_available_port(start_port):
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            try:
                sock.bind(('localhost', port + 1))
                return (port, port + 1)
            except OSError as e:
                if e.errno == 98:  # "Address already in use"
                    port += 2
                else:
                    raise e

class StopVMView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, uuid):
        # Authenticate user using API key
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


class StartVMView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, uuid):
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
