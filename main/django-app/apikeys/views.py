import os
import re
import subprocess
import socket
import glob
import time
from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ApiKey
from subprocess import CalledProcessError
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework import status
from .models import ApiKey
import os
import json
import shutil
import psutil
import asyncio
from asgiref.sync import async_to_sync
from asgiref.sync import sync_to_async
from qemu.qmp import QMPClient
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import FileResponse
import zipfile
from PIL import Image
import datetime
from datetime import datetime
import glob

#User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
class RemoveVMDateTimeView(View):
    authentication_classes = []
    permission_classes = []

    async def post(self, request):
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


@method_decorator(csrf_exempt, name='dispatch')
class ChangeVMDateTimeView(View):
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

def validate_date(date_str):
    """
    Function to validate the date string against the format 'YYYY-MM-DDTHH:MM:SS'
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
        return True
    except ValueError:
        return False

@method_decorator(csrf_exempt, name='dispatch')
class DownloadNetworkPcapView(View):
    authentication_classes = []
    permission_classes = []

    async def get(self, request, uuid):
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



@method_decorator(csrf_exempt, name='dispatch')
class CheckTapInterfaceView(View):
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


@method_decorator(csrf_exempt, name='dispatch')
class StartTapInterfaceView(View):
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

        # Start the tap interface
        start_tap_cmd = f"ifconfig {tap_interface} up"
        start_tap_process = subprocess.Popen(start_tap_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        start_tap_output, start_tap_error = start_tap_process.communicate()

        if start_tap_error:
            return JsonResponse({'error': f'Error starting tap interface: {start_tap_error}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return JsonResponse({'message': f'Tap interface {tap_interface} started successfully'}, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class StopTapInterfaceView(View):
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

        # Start the tap interface
        start_tap_cmd = f"ifconfig {tap_interface} down"
        start_tap_process = subprocess.Popen(start_tap_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        start_tap_output, start_tap_error = start_tap_process.communicate()

        if start_tap_error:
            return JsonResponse({'error': f'Error stopping tap interface: {start_tap_error}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return JsonResponse({'message': f'Tap interface {tap_interface} stopped successfully'}, status=status.HTTP_200_OK)


def get_available_memory():
    mem_info = psutil.virtual_memory()
    available_memory = mem_info.available / 1024 / 1024  # Convert to MB
    return available_memory

@method_decorator(csrf_exempt, name='dispatch')
class GetAvailableMemoryView(View):
    def get(self, request):
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


@method_decorator(csrf_exempt, name='dispatch')
class ChangeMemorySizeView(View):
    def post(self, request, uuid):
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


#@method_decorator(csrf_exempt, name='dispatch')
class MemorySizeView(View):
    def get(self, request, uuid):
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

async def delete_snapshot(uuid, snapshot_name):
    qmp = QMPClient('forensicVM')
    socket_path = f"/forensicVM/mnt/vm/{uuid}/run/qmp.sock"

    try:
        await qmp.connect(socket_path)
        await qmp.execute("human-monitor-command", {
            "command-line": f"delvm {snapshot_name}"
        })
        return "Snapshot deleted."
    except Exception as e:
        print(e)
        return "Error deleting snapshot."
    finally:
        await qmp.disconnect()


@method_decorator(csrf_exempt, name='dispatch')
class DeleteSnapshotView(View):
    async def post(self, request, uuid):
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


async def rollback_snapshot(uuid, snapshot_name):
    qmp = QMPClient('forensicVM')
    socket_path = f"/forensicVM/mnt/vm/{uuid}/run/qmp.sock"

    try:
        await qmp.connect(socket_path)
        await qmp.execute("human-monitor-command", {
            "command-line": f"loadvm {snapshot_name}"
        })
        return "Snapshot rollback successful."
    except Exception as e:
        print(e)
        return "Error rolling back snapshot."
    finally:
        await qmp.disconnect()

@method_decorator(csrf_exempt, name='dispatch')
class RollbackSnapshotView(View):
    async def post(self, request, uuid):
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


async def create_snapshot(uuid):
    qmp = QMPClient('forensicVM')
    socket_path = f"/forensicVM/mnt/vm/{uuid}/run/qmp.sock"

    try:
        await qmp.connect(socket_path)
        snapshot_name = datetime.datetime.now().strftime("snap-%Y-%m-%d_%H:%M:%S")
        await qmp.execute("human-monitor-command", {
            "command-line": f"savevm {snapshot_name}"
        })
        return snapshot_name
    except Exception as e:
        print(e)
        return "Error creating snapshot."
    finally:
        await qmp.disconnect()


@method_decorator(csrf_exempt, name='dispatch')
class CreateSnapshotView(View):
    async def post(self, request, uuid):
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



async def get_snapshots(uuid):
    qmp = QMPClient('forensicVM')
    socket_path = f"/forensicVM/mnt/vm/{uuid}/run/qmp.sock"
    snapshots = []

    try:
        await qmp.connect(socket_path)
        result = await qmp.execute("human-monitor-command", {
            "command-line": "info snapshots"
        })
        
        # Assuming that result is a string with a table-like structure
        snapshot_lines = result.split('\n')
        for line in snapshot_lines:
            # DEBUG
            print(line)
            if line.startswith('--'):
                snapshot_info = line.split()
                snapshot_id = snapshot_info[0]
                snapshot_tag = snapshot_info[1]
                vm_size = snapshot_info[2]
                date = snapshot_info[3]
                vm_clock = snapshot_info[4]
                snapshots.append({
                    'id': snapshot_id,
                    'tag': snapshot_tag,
                    'vm_size': vm_size,
                    'date': date,
                    'vm_clock': vm_clock
                })
    except Exception as e:
        print(e)
    finally:
        await qmp.disconnect()

    return snapshots

@method_decorator(csrf_exempt, name='dispatch')
class SnapshotListView(View):
    async def get(self, request, uuid):
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


def create_and_format_qcow2(qcow2_file, folders):
    # Create a new QCOW2 file with 20GB of space
    subprocess.run(['qemu-img', 'create', '-f', 'qcow2', qcow2_file, '20G'], check=True)

    # Name for the label
    label_name = "possible evidence"

    # Create a new NTFS partition with guestfish
    guestfish_commands = f"""
    launch
    part-init /dev/sda mbr
    part-add /dev/sda p 2048 -1024
    part-set-mbr-id /dev/sda 1 0x07
    mkfs ntfs /dev/sda1
    set-label /dev/sda1 "{label_name}"
    mount /dev/sda1 /
    """

    # Create folders using guestfish
    for folder in folders:
        guestfish_commands += f"mkdir /{folder}\n"
        print(folder)

    guestfish_commands += """
    umount /
    """



    command = f"guestfish --rw -a {qcow2_file} <<EOF\n{guestfish_commands}\nEOF\n"
    subprocess.run(command, shell=True, check=True)

    guestfish_commands = """
    launch
    mount /dev/sda1 /
    write /readme.txt \"Forensic VM: This drive was automaticaly created. Please put the probable evidence inside the sub-folders with the same tag of autopsy software for the easiest classification\"
    write /leiame.txt \"Forensic VM: Este disco foi criado automáticamente. Para facilitar a classificação, por favor coloque as evidências recolhidas nas subpastas que têm o mesmo nome que a etiqueta no software autopsy\"
    umount /
    """

    command = f"guestfish --rw -a {qcow2_file} <<EOF\n{guestfish_commands}\nEOF\n"
    subprocess.run(command, shell=True, check=True)

    print("END guestfish")




@method_decorator(csrf_exempt, name='dispatch')
class RecreateFoldersView(View):
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





class RunPluginView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
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


class ListPluginsView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
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


def get_plugin_info(plugin_dir, info):
    run_script_path = os.path.join('/forensicVM/plugins', plugin_dir, 'run.sh')
    result = subprocess.run(['bash', run_script_path, 'info'], capture_output=True, text=True)
    output = result.stdout.strip()

    try:
        info_dict = json.loads(output)
    except json.JSONDecodeError:
        info_dict = {}

    return info_dict.get(info, '')

async def insert_network_card(uuid, mac_address=None):
    if not mac_address:
        # Generate a random MAC address if not supplied
        mac_address = generate_random_mac_address()

    qmp = QMPClient('forensicVM')
    socket_path = f"/forensicVM/mnt/vm/{uuid}/run/qmp.sock"

    try:
        await qmp.connect(socket_path)
#        res = await qmp.execute("human-monitor-command",
#                                {"command-line": f"device_add virtio-net-pci,netdev=net0,mac={mac_address}"})
#        res = await qmp.execute("device_add",{"driver=e100 id=net1"})
#        res = await qmp.execute("device_add",
#                                { "driver": "virtio-net-pci",
#                                  "id": "net0",
#                                  "bus": "pci0.1",
#                                  "mac": f"{mac_address}"})

#        res = await qmp.execute("guest-exec",
#                                { "path": "c:/windows/cmd.exe",
#                                  "arg": "/p"})

        res = await qmp.execute("netdev_add",
                                { "type": "user",
                                  "id": "net0"})
        res = await qmp.execute("device_add",
                                { "driver": "virtio-net-pci",
                                  "netdev": "net0"})
        res = await qmp.execute("query-pci", {})
        print(res)

#-netdev user,id=net0 -device virtio-net-pci,netdev=net0
#{ "execute": "netdev_add", "arguments": { "type": "user", "id": "netdev1" } }

        print(f"Network card inserted with MAC address: {mac_address}")
    except Exception as e:
        print(e)
    finally:
        await qmp.disconnect()

    return "Network card inserted."

def generate_random_mac_address():
    # Generate a random MAC address using your preferred logic
    # Example implementation:
    import random

    mac = [0x52, 0x54, 0x00,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]

    mac_address = ':'.join(map(lambda x: "%02x" % x, mac))
    return mac_address

@method_decorator(csrf_exempt, name='dispatch')
class InsertNetworkCardView(View):
    authentication_classes = []
    permission_classes = []

    async def get(self, request, uuid):
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

        #uuid = request.GET.get('uuid')
        #uuid = self.kwargs.get('uuid')

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


async def insert_cdrom(uuid, filename):
    qmp = QMPClient('forensicVM')
    socket_path = f"/forensicVM/mnt/vm/{uuid}/run/qmp.sock"

    try:
        await qmp.connect(socket_path)
        res = await qmp.execute("blockdev-change-medium",
                                { "id": "ide0-0-0",
                                  "filename": f"/forensicVM/mnt/iso/{filename}",
                                  "format": "raw" })
        print(f"CD-ROM inserted.")
    except Exception as e:
        print(e)
    finally:
        await qmp.disconnect()

    return "CD-ROM inserted."


@method_decorator(csrf_exempt, name='dispatch')
class InsertCDROMView(View):
    authentication_classes = []
    permission_classes = []

    async def get(self, request, uuid, filename):
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

        cdrom_status = await insert_cdrom(uuid, filename)
        return JsonResponse({'message': cdrom_status}, status=status.HTTP_200_OK)


async def eject_cdrom(uuid):
    qmp = QMPClient('forensicVM')
    socket_path = f"/forensicVM/mnt/vm/{uuid}/run/qmp.sock"

    try:
        await qmp.connect(socket_path)
        #res = await qmp.execute("human-monitor-command",
        #                        { "command-line": "eject ide0-0-0" })
        res = await qmp.execute("blockdev-open-tray",
                                { "id": "ide0-0-0"})
        print(f"CD-ROM ejected.")
    except Exception as e:
        print(e)
    finally:
        await qmp.disconnect()

    return "CD-ROM ejected."

@method_decorator(csrf_exempt, name='dispatch')
class EjectCDROMView(View):
    authentication_classes = []
    permission_classes = []

    async def get(self, request, uuid):
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

        cdrom_status = await eject_cdrom(uuid)
        return JsonResponse({'message': cdrom_status}, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class DeleteISOFileView(View):
    authentication_classes = []
    permission_classes = []

    def post(self, request, filename):
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


@method_decorator(csrf_exempt, name='dispatch')
class UploadISOView(View):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
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


class ListISOFilesView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
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


def change_qcow2(qcow2_file, folders):

    # Create a new NTFS partition with guestfish
    guestfish_commands = f"""
    launch
    mount /dev/sda1 /
    """

    # Create folders using guestfish
    for folder in folders:
        guestfish_commands += f"-mkdir /{folder} \n"
        print(folder)

    guestfish_commands += """
    umount /
    """



    command = f"guestfish --rw -a {qcow2_file} <<EOF\n{guestfish_commands}\nEOF\n"
    subprocess.run(command, shell=True, check=True)

    guestfish_commands = """
    launch
    mount /dev/sda1 /
    write /readme.txt \"Forensic VM: This drive was automaticaly created. Please put the probable evidence inside the sub-folders with the same tag of autopsy software for the easiest classification\"
    write /leiame.txt \"Forensic VM: Este disco foi criado automáticamente. Para facilitar a classificação, por favor coloque as evidências recolhidas nas subpastas que têm o mesmo nome que a etiqueta no software autopsy\"
    umount /
    """

    command = f"guestfish -x --rw -a {qcow2_file} <<EOF\n{guestfish_commands}\nEOF\n"
    subprocess.run(command, shell=True, check=True)

    print("END guestfish")


@method_decorator(csrf_exempt, name='dispatch')
class CreateFoldersView(View):
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

        # Check if vmdk_file exists
        if not os.path.exists(qcow2_file):
            return JsonResponse({'error': f'QCOW2 file {qcow2_file} not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Create the folders using guestfish
            #guestfish_commands = '\n'.join([f'! mkdir /{folder} || true' for folder in folders])
            ##command = f"""
            #guestfish --rw -a {qcow2_file} <<EOF
            #run
            #ntfsfix /dev/sda1
            #mount /dev/sda1 /
            #{guestfish_commands}
            #umount /
            #EOF
            #"""
            #os.system(command)
            #subprocess.run(command, shell=True, check=True)
            change_qcow2(qcow2_file, folders)

            return JsonResponse({'message': f'Folders {", ".join(folders)} created successfully in {qcow2_file}'}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': f'Error executing guestfish: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






@method_decorator(csrf_exempt, name='dispatch')
class DownloadEvidenceView(View):
    authentication_classes = []
    permission_classes = []

    async def get(self, request, uuid):
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

async def memory_snapshot(uuid):
    qmp = QMPClient('forensicVM')
    socket_path = f"/forensicVM/mnt/vm/{uuid}/run/qmp.sock"
    memory_snapshots_path = f"/forensicVM/mnt/vm/{uuid}/memory/"

    if not os.path.exists(memory_snapshots_path):
        os.makedirs(memory_snapshots_path)

    existing_snapshots = sorted(glob.glob(f"{memory_snapshots_path}/memory_snapshot*.dmp"))
    next_snapshot_number = len(existing_snapshots) + 1
    next_snapshot_filename = f"memory_snapshot{next_snapshot_number:03d}.dmp"
    next_snapshot_path = os.path.join(memory_snapshots_path, next_snapshot_filename)

    try:
        await qmp.connect(socket_path)
        res = await qmp.execute('dump-guest-memory', { "paging": False, "protocol": f"file:{next_snapshot_path}", "detach": False})
        print(f"Memory snapshot saved: {next_snapshot_path}")
    except Exception as e:
        print(e)
    finally:
        await qmp.disconnect()

    return next_snapshot_path

@method_decorator(csrf_exempt, name='dispatch')
class MemorySnapshotView(View):
    authentication_classes = []
    permission_classes = []

    async def get(self, request, uuid):
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

        #snapshot_file = async_to_sync(memory_snapshot)(uuid)
        snapshot_file = await memory_snapshot(uuid)
        response = FileResponse(open(snapshot_file, 'rb'), content_type='application/octet-stream', as_attachment=True, filename=os.path.basename(snapshot_file))
        return response

@method_decorator(csrf_exempt, name='dispatch')
class DownloadScreenshotsView(View):
    authentication_classes = []
    permission_classes = []

    async def get(self, request, uuid):
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



async def screendump(uuid):
    qmp = QMPClient('forensicVM')
    socket_path = f"/forensicVM/mnt/vm/{uuid}/run/qmp.sock"
    screenshots_path = f"/forensicVM/mnt/vm/{uuid}/screenshots/"

    if not os.path.exists(screenshots_path):
        os.makedirs(screenshots_path)

    existing_screenshots = sorted(glob.glob(f"{screenshots_path}/sc*.png"))
    next_screenshot_number = len(existing_screenshots) + 1
    next_screenshot_filename = f"sc{next_screenshot_number:05d}.png"
    next_screenshot_path = os.path.join(screenshots_path, next_screenshot_filename)

    try:
        await qmp.connect(socket_path)
        res = await qmp.execute('screendump', {"filename": next_screenshot_path})
        print(f"Screenshot saved: {next_screenshot_path}")
    except Exception as e:
        print(e)
    finally:
        await qmp.disconnect()
#
#@method_decorator(csrf_exempt, name='dispatch')
#class ScreenshotVMView(View):
#    authentication_classes = []
#    permission_classes = []
#
#    async def post(self, request, uuid):
#        api_key = request.META.get('HTTP_X_API_KEY')
#        if api_key:
#            try:
#                api_key = await sync_to_async(ApiKey.objects.get)(key=api_key)
#                user = await sync_to_async(getattr)(api_key, 'user')
#                if not user.is_active:
#                    return JsonResponse({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
#            except ApiKey.DoesNotExist:
#                return JsonResponse({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
#        else:
#            return JsonResponse({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)
#
#        vm_path = f"/forensicVM/mnt/vm/{uuid}"
#        vm_exists = os.path.exists(vm_path)
#
#        if not vm_exists:
#            return JsonResponse({'error': f'VM with UUID {uuid} not found'}, status=status.HTTP_404_NOT_FOUND)
#
#        await screendump(uuid)
#
#        result = {'screenshot_taken': True, 'message': f'Screenshot taken for VM with UUID {uuid}'}
#
#        return JsonResponse(result, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class ScreenshotVMView(View):
    authentication_classes = [SessionAuthentication]                # ADDED
    #authentication_classes = []
    permission_classes = []

    async def post(self, request, uuid):
        user, api_key_error = await sync_to_async(self.get_user_or_key_error)(request)
        if api_key_error:
            return api_key_error

        vm_path = f"/forensicVM/mnt/vm/{uuid}"
        vm_exists = await sync_to_async(os.path.exists)(vm_path)

        if not vm_exists:
            return JsonResponse({'error': f'VM with UUID {uuid} not found'}, status=status.HTTP_404_NOT_FOUND)

        await screendump(uuid)

        result = {'screenshot_taken': True, 'message': f'Screenshot taken for VM with UUID {uuid}'}

        return JsonResponse(result, status=status.HTTP_200_OK)


    def get_user_or_key_error(self, request):
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
#
#@method_decorator(csrf_exempt, name='dispatch')
#class ShutdownVMView(View):
#    authentication_classes = [SessionAuthentication]                # ADDED
#    permission_classes = []
#
#    async def post(self, request, uuid):
#        api_key = request.META.get('HTTP_X_API_KEY')
#        user = getattr(request, 'user', None)                       # IF sync
#        #user = await sync_to_async(getattr)(request, 'user', None)  # ASYNC: Get the user in the request
#        if user and user.is_authenticated:                          # User is authenticated via session
#            print("DEBUG: USER AUTHENTICATED")
#            pass                                                    # Add this extra block to the request
#        elif api_key:                                               # <--- Changed
#            try:
#                api_key = await sync_to_async(ApiKey.objects.get)(key=api_key)
#                user = await sync_to_async(getattr)(api_key, 'user')
#                if not user.is_active:
#                    return JsonResponse({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
#            except ApiKey.DoesNotExist:
#                return JsonResponse({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
#        else:
#            return JsonResponse({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)
#
#        vm_path = f"/forensicVM/mnt/vm/{uuid}"
#        vm_exists = os.path.exists(vm_path)
#
#        if not vm_exists:
#            return JsonResponse({'error': f'VM with UUID {uuid} not found'}, status=status.HTTP_404_NOT_FOUND)
#
#        await system_shutdown(uuid)
#
#        result = {'vm_shutdown': True, 'message': f'Shutdown command sent to VM with UUID {uuid}'}
#
#        return JsonResponse(result, status=status.HTTP_200_OK)
#

@method_decorator(csrf_exempt, name='dispatch')
class ShutdownVMView(View):
    authentication_classes = [SessionAuthentication]
    permission_classes = []

    async def post(self, request, uuid):
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

#@method_decorator(csrf_exempt, name='dispatch')
#class ResetVMView(View):
#    authentication_classes = [SessionAuthentication]                # ADDED
#    permission_classes = []
#
#    async def post(self, request, uuid):
#        api_key = request.META.get('HTTP_X_API_KEY')
#        #user = getattr(request, 'user', None)                       # IF sync
#        user = await sync_to_async(getattr)(request, 'user', None)  # ASYNC: Get the user in the request
#        if user and user.is_authenticated:                          # User is authenticated via session
#            print("DEBUG: USER AUTHENTICATED")
#            pass                                                    # Add this extra block to the request
#        elif api_key:                                               # <--- Changed
#        #if api_key:
#            try:
#                api_key = await sync_to_async(ApiKey.objects.get)(key=api_key)
#                user = await sync_to_async(getattr)(api_key, 'user')
#                #user = api_key.user
#                if not user.is_active:
#                    return JsonResponse({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
#            except ApiKey.DoesNotExist:
#                return JsonResponse({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)
#        else:
#            return JsonResponse({'error': 'API key required'}, status=status.HTTP_401_UNAUTHORIZED)
#
#        vm_path = f"/forensicVM/mnt/vm/{uuid}"
#        vm_exists = os.path.exists(vm_path)
#
#        if not vm_exists:
#            return JsonResponse({'error': f'VM with UUID {uuid} not found'}, status=status.HTTP_404_NOT_FOUND)
#
#        await system_reset(uuid)
#
#        result = {'vm_reset': True, 'message': f'Reset command sent to VM with UUID {uuid}'}
#
#        return JsonResponse(result, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class ResetVMView(View):
    authentication_classes = [SessionAuthentication]
    permission_classes = []

    async def post(self, request, uuid):
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

        #vm_path = f"/forensicVM/mnt/vm/{uuid}"
        vm_path = f"/forensicVM/mnt/vm/{uuid}/mode"
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
    authentication_classes = [SessionAuthentication]                # ADDED
    permission_classes = []

    def post(self, request, uuid):
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


class StartVMView(APIView):
    authentication_classes = [SessionAuthentication]                # ADDED
    permission_classes = []

    def post(self, request, uuid):
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

class ForensicImageVMStatus(APIView):
    authentication_classes = [SessionAuthentication]                # ADDED
    #authentication_classes = []
    permission_classes = []

    def get(self, request, uuid):
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
