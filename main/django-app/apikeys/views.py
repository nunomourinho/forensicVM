import os
import re
import subprocess
import socket
import glob
import time
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user
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
from .models import ApiKey, ChainOfCustody
import json
import shutil
import psutil
import asyncio
from asgiref.sync import async_to_sync
from asgiref.sync import sync_to_async
from apscheduler.schedulers.asyncio import AsyncIOScheduler
try:
    import asyncio
except ImportError:
    import trollius as asyncio
from django.http import HttpResponseBadRequest
from django.utils.decorators import method_decorator
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
from os.path import basename, join, isfile
from django.http import Http404
from urllib.parse import quote
import cv2
from channels.db import database_sync_to_async
from django.http import HttpResponse
from docx import Document
from docx.shared import Pt
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from .models import ChainOfCustody
from .models import VMData
import io
import aiofiles
import xml.etree.ElementTree as ET
from excel_response import ExcelResponse
import xlwt
import pandas as pd
from scipy.stats import pointbiserialr
from statsmodels.formula.api import ols
import statsmodels.api as sm
from docx import Document


@method_decorator(csrf_exempt, name='dispatch')
class GenerateMetrics(View):
    """
    View class to generate a Word document directly from VMData objects.

    This view is CSRF exempt similar to the provided example.
    """

    def get(self, request, *args, **kwargs):
        """
        Handles the GET request to fetch all VMData objects, analyze them, and return a Word document.

        Args:
            request (HttpRequest): The HTTP GET request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            FileResponse: A Word formatted response containing the analysis of VMData objects.
        """
        # Fetching the data and converting it to DataFrame
        queryset = VMData.objects.all().values()
        data = pd.DataFrame.from_records(queryset)

        # Call the function to generate the docx and latex
        doc_path = self.analyze_virtualization_metrics_final(data)

        return FileResponse(open(doc_path, 'rb'), as_attachment=True, filename='virtualization_metrics_analysis.docx')

    def analyze_virtualization_metrics_final(self, data):
        doc = Document()
        doc.add_heading('Virtualization Metrics Analysis', 0)

        try:
            # 2. Data Analysis
            descriptive_stats = data.groupby(['Tool used to mount image', 'Conversion mode'])['Real conversion time in seconds'].describe()
            doc.add_heading('Descriptive Statistics', level=1)
            table = doc.add_table(rows=1, cols=9)
            hdr_cells = table.rows[0].cells
            columns = ['Tool', 'Mode', 'count', 'mean', 'std', 'min', '25%', '50%', 'max']
            for i, col in enumerate(columns):
                hdr_cells[i].text = col.capitalize()

            for index, row in descriptive_stats.iterrows():
                cells = table.add_row().cells
                cells[0].text = str(index[0])
                cells[1].text = str(index[1])
                for i in range(2, 9):
                    cells[i].text = str(round(row[columns[i]], 2))
        except Exception as e:
            doc.add_paragraph(f"Error during Descriptive Statistics: {e}")

        try:
            data['Tool_Binarized'] = data['Tool used to mount image'].apply(lambda x: 0 if x == 'aff' else 1)
            correlation, p_value = pointbiserialr(data['Tool_Binarized'], data['Real conversion time in seconds'])

            doc.add_heading('Point-biserial Correlation', level=1)
            doc.add_paragraph(f'Correlation: {correlation:.3f}')
            doc.add_paragraph(f'p-value: {p_value:.3f}')
        except Exception as e:
            doc.add_paragraph(f"Error during Point-biserial Correlation: {e}")

        try:
            data_renamed = data.rename(columns={
                'Real conversion time in seconds': 'ConversionTime',
                'Tool used to mount image': 'Tool',
                'Conversion mode': 'Mode'
            })
            model_renamed = ols('ConversionTime ~ C(Tool) * C(Mode)', data=data_renamed).fit()
            anova_table_renamed = sm.stats.anova_lm(model_renamed, typ=2)
            
            doc.add_heading('ANOVA Results', level=1)
            table = doc.add_table(rows=1, cols=4)
            hdr_cells = table.rows[0].cells
            columns = ['Source', 'sum_sq', 'df', 'F']
            for i, col in enumerate(columns):
                hdr_cells[i].text = col.capitalize()

            for index, row in anova_table_renamed.iterrows():
                cells = table.add_row().cells
                cells[0].text = str(index)
                for i in range(1, 4):
                    cells[i].text = str(round(row[columns[i]], 2))
        except Exception as e:
            doc.add_paragraph(f"Error during ANOVA Results: {e}")

        doc_path = "virtualization_metrics_analysis_final.docx"
        doc.save(doc_path)
        
#        latex_content = "\\section*{Virtualization Metrics Analysis}\n"
        
#        try:
#            latex_content += "\\subsection*{Descriptive Statistics}\n"
#            latex_content += descriptive_stats.to_latex()
#            latex_content += "\n\\subsection*{Point-biserial Correlation}\n"
#            latex_content += f"Correlation: {correlation:.3f}\n\np-value: {p_value:.3f}\n"
#            latex_content += "\n\\subsection*{ANOVA Results}\n"
#            latex_content += anova_table_renamed.to_latex()
#        except Exception as e:
#            latex_content += f"\\paragraph*{Error during LaTeX generation: {e}}"

#        latex_path = "virtualization_metrics_analysis_final.tex"
#        with open(latex_path, 'w') as latex_file:
#            latex_file.write(latex_content)

        return doc_path
#, latex_path


@method_decorator(csrf_exempt, name='dispatch')
class ExportVMDataToExcel(View):
    """
    View class to export VMData objects to an Excel format.
    
    This view is CSRF exempt to accommodate external tools or systems that might need to fetch the Excel 
    without having a CSRF token. It provides an endpoint that responds with an Excel file containing VMData 
    records.
    """

    def get(self, request, *args, **kwargs):
        """
        Handles the GET request to fetch all VMData objects and return them as an Excel response.

        Args:
            request (HttpRequest): The HTTP GET request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: An Excel formatted response containing all VMData objects.
        """
        queryset = VMData.objects.all()
        return ExcelResponse(queryset)


def ExcelResponse(queryset):
    """
    Generate an Excel response given a Django queryset.

    The function creates an Excel workbook with one worksheet named "VMData". The headers of the worksheet
    are based on the `verbose_name` of the model fields. Each row after the header contains the values 
    corresponding to a record in the queryset.

    Args:
        queryset (QuerySet): A Django queryset containing the records to be exported.

    Returns:
        HttpResponse: An HTTP response containing the Excel file with the VMData records.
    """
    
    model = queryset.model
    field_names = [field.name for field in model._meta.fields]

    # Fetch verbose_names for each field
    headers = [field.verbose_name for field in model._meta.fields]

    # Create a new Excel workbook and add a worksheet
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Metrics")

    # Write headers to the worksheet
    for col_num, header in enumerate(headers):
        ws.write(0, col_num, header)

    # Write data to the worksheet
    for row_num, record in enumerate(queryset, start=1):
        for col_num, field_name in enumerate(field_names):
            value = getattr(record, field_name)
            ws.write(row_num, col_num, value)

    # Prepare response
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="virtualization_metrics.xls"'
    wb.save(response)

    return response



@method_decorator(csrf_exempt, name='dispatch')
class InsertMetrics(View):
    """
    This view is responsible for inserting metrics related to a virtual machine.
    It reads data from specific files located in a given directory and saves them into the VMData model.
    """

    authentication_classes = [SessionAuthentication]
    permission_classes = []

    def post(self, request, uuid):
        """
        Handles the POST request. Reads metrics from files in the specified directory
        and saves them to the VMData model. If a file doesn't exist, default values will be set.

        Args:
            request (HttpRequest): The incoming HTTP POST request.
            uuid (str): The UUID of the virtual machine.

        Returns:
            HttpResponse: A 200 status response after successful data insertion.
        """

        user, api_key_error = self.get_user_or_key_error(request)
        request.user, api_key_error = self.get_user_or_key_error(request)

        if api_key_error:
            return api_key_error

        vm_data = VMData(uuid=uuid)

        BASE_DIR = f"/forensicVM/mnt/vm/{uuid}/stats"
        INFO_DIR = f"/forensicVM/mnt/vm/{uuid}/"

        # File names separated based on extension
        string_files_no_ext = ['conversion_time_txt', 'extension', 'filename', 'image_type', 'mode', "start_time_full", "end_time_full"]
        float_files_no_ext = ['conversion_time_in_seconds', 'image_size']
        float_files_txt_ext = ['disk_read', 'disk_write', 'elapsed_time', 'end_time', 'start_time', 'transfer_read_speed']

        # Process string data without extension
        for file in string_files_no_ext:
            file_path = os.path.join(BASE_DIR, file)
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    line = f.readline().strip()
                    setattr(vm_data, file, line if line else "N/A")
            else:
                setattr(vm_data, file, "N/A")

        # Process float data without extension
        for file in float_files_no_ext:
            file_path = os.path.join(BASE_DIR, file)
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    line = f.readline().strip()
                    setattr(vm_data, file, float(line) if line else 0.0)
            else:
                setattr(vm_data, file, 0.0)

        # Process float data with .txt extension
        for file in float_files_txt_ext:
            file_path = os.path.join(BASE_DIR, file + '.txt')
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    line = f.readline().strip()
                    setattr(vm_data, file, float(line) if line else 0.0)
            else:
                setattr(vm_data, file, 0.0)

        # Extract additional fields using the logic in VMListView
        info_file_path = os.path.join(INFO_DIR, f"{uuid}.info")
        if os.path.exists(info_file_path):
            tree = ET.parse(info_file_path)
            root = tree.getroot()

            # Find the first <operatingsystem> under <operatingsystems>
            os_data = root.find('./operatingsystem')
            if os_data:
                vm_data.distro = os_data.findtext('distro', "N/A")
                vm_data.hostname = os_data.findtext('hostname', "N/A")
                vm_data.osinfo = os_data.findtext('osinfo', "N/A")
                vm_data.product_name = os_data.findtext('product_name', "N/A")
        else:
            vm_data.distro = "N/A"
            vm_data.hostname = "N/A"
            vm_data.osinfo = "N/A"
            vm_data.product_name = "N/A"

        vm_data.save()
        sync_create_chain_of_custody_record(request, "Converted image to ForensicVM", "Converted the image to forensic VM and collected performance metrics", uuid)
        return HttpResponse(status=200)

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



async def memory_snapshot_helper(uuid):
    """
    This asynchronous function captures a snapshot of a VM's memory.

    It establishes a connection with the QEMU Machine Protocol (QMP) running on the VM,
    then uses the QMP command 'dump-guest-memory' to capture the memory snapshot.

    The function saves the memory snapshot to the VM's directory, with a unique filename
    based on the current number of existing snapshots.

    Parameters:
    uuid (str): The UUID of the VM.

    Returns:
    str: The path to the newly created memory snapshot file.

    Raises:
    Exception: If there's an error executing the 'dump-guest-memory' command or disconnecting from QMP.
    """
    qmp = QMPClient('forensicVM')
    socket_path = f"/forensicVM/mnt/vm/{uuid}/run/qmp.sock"
    memory_snapshots_path = f"/forensicVM/mnt/vm/{uuid}/memory/"

    if not os.path.exists(memory_snapshots_path):
        os.makedirs(memory_snapshots_path)

    next_snapshot_filename = f"memory_snapshot_analysis.dmp"
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


class VirtualIntrospectionView(View):
    """
    A class-based view that handles virtual introspection requests.

    This view fetches process lists, possible malware detections, network connections,
    and other related information from a given virtual machine snapshot, using the Volatility3
    forensic analysis tool. It then presents this information in a rendered HTML template.
    """

    async def get(self, request, uuid):
        """
        Handles the GET request for virtual introspection based on the provided VM's UUID.

        Args:
            request (HttpRequest): The Django HttpRequest object.
            uuid (str): The UUID of the virtual machine to introspect.

        Returns:
            HttpResponse: A rendered HTML page with the introspection data or a JSON error response.

        Raises:
            Exception: If there's an error executing the Volatility3 command.
        """
        is_active = await sync_to_async(lambda: request.user.is_active)()

        if not is_active:
            return JsonResponse({'error': 'User account is disabled.'}, status=401)

        await async_create_chain_of_custody_record(request, "Virtual introspect", "Generated report on live process lists, possible malware and network connections", uuid)

        snapshot_file = await memory_snapshot_helper(uuid)

        # Run the vol.py command in a shell
        cmd = [
            'python3', '/forensicVM/bin/volatility3/vol.py',
            '-f', snapshot_file,
            'windows.pstree'
        ]

        # Execute the command and fetch the result
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # If the command failed, raise an error
        #if result.returncode != 0:
        #    raise Exception("Error executing vol.py: " + result.stderr)

        # Parse the result stdout

        try:
           lines = result.stdout.splitlines()[4:]  # skip the first 4 lines
        except Exception as e:
           lines = []

        headers = ["PID", "PPID", "ImageFileName", "Offset(V)", "Threads", "Handles", "SessionId", "Wow64", "CreateTime", "ExitTime", "-", "-"]
        processes = []

        for line in lines:
            data = re.split(r'\s+', line.strip())  # split using regex to handle indeterminate spaces
            #if len(data) == 10:  # We expect 10 columns
            print(data)
            processes.append(data)

        #context = {
        #    'headers': headers,
        #    'processes': processes
        #}

        cmd_malfind = ['python3', '/forensicVM/bin/volatility3/vol.py', '-f', snapshot_file, 'windows.malfind']
        malfind_output = subprocess.Popen(cmd_malfind, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).communicate()[0]

        cmd_envars = ['python3', '/forensicVM/bin/volatility3/vol.py', '-f', snapshot_file, 'windows.envars']
        envars_output = subprocess.Popen(cmd_envars, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).communicate()[0]

        cmd_envars = ['python3', '/forensicVM/bin/volatility3/vol.py', '-f', snapshot_file, 'windows.cmdline']
        cmdline_output = subprocess.Popen(cmd_envars, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).communicate()[0]

        cmd_netscan = ['python3', '/forensicVM/bin/volatility3/vol.py', '-f', snapshot_file, 'windows.netscan']
        netscan_output = subprocess.Popen(cmd_netscan, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).communicate()[0]

        cmd_netstat = ['python3', '/forensicVM/bin/volatility3/vol.py', '-f', snapshot_file, 'windows.netstat']
        netstat_output = subprocess.Popen(cmd_netstat, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).communicate()[0]

        context = {"processes": processes, "headers": headers, "malfind_output": malfind_output, "envars_output": envars_output, "cmdline_output": cmdline_output, "netscan_output": netscan_output, "netstat_output": netstat_output}

        return await sync_to_async(render)(request, 'introspect.html', context)


def get_client_port(request):
    """
    Extract the client's port from the request.
    """
    return request.META.get('REMOTE_PORT')

def get_client_ip(request):
    """
    Extract the client's IP address from the request.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    else:
        return request.META.get('REMOTE_ADDR')

# Async version on the create chain of custody
@database_sync_to_async
def async_create_chain_of_custody_record(request, action, parameters, uuid_value):
    """
    Create a ChainOfCustody record using provided action, parameters, and uuid.
    Also capture the client's IP address.
    """
    ip_address = get_client_ip(request)
    ip_port = get_client_port(request)

    record = ChainOfCustody(
        user=request.user,
        action=action,
        parameters=parameters,
        ip_address=ip_address,
        ip_port=ip_port,
        uuid=uuid_value,
    )
    record.save()

# sync version on the create chain of custody
def sync_create_chain_of_custody_record(request, action, parameters, uuid_value):
    """
    Create a ChainOfCustody record using provided action, parameters, and uuid.
    Also capture the client's IP address.
    """
    ip_address = get_client_ip(request)
    ip_port = get_client_port(request)

    record = ChainOfCustody(
        user=request.user,
        action=action,
        parameters=parameters,
        ip_address=ip_address,
        ip_port=ip_port,
        uuid=uuid_value,
    )
    record.save()


class GenerateChainOfCustodyView(View):
    """
    A class-based view that generates a chain of custody record in the form of a Word document.

    This view fetches the chain of custody records associated with a given UUID from the database,
    creates a formatted Word document presenting these records, and then returns this document 
    to the user.
    """

    def get(self, request, uuid, *args, **kwargs):
        """
        Handles the GET request to generate the chain of custody Word document based on the provided UUID.

        Args:
            request (HttpRequest): The Django HttpRequest object.
            uuid (str): The UUID associated with the desired chain of custody records.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: A Word document (.docx) containing the chain of custody records for the specified UUID.

        Notes:
            The resulting Word document is formatted with a centered logo, a title, and a table 
            presenting the chain of custody records. Each record includes user, date, action, 
            parameters, UUID, and IP address. 
        """
        # Filter ChainOfCustody records by uuid
        records = ChainOfCustody.objects.filter(uuid=uuid)

        # Create a new Document
        doc = Document()
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture('/forensicVM/main/branding/ForensicVMblack.jpg', width=Inches(2.0))
        doc.add_heading('Chain of Custody Records', 0)

        # Add a table to the Document
        table = doc.add_table(rows=1, cols=6)
        table.style = 'Medium List 1'

        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Date'
        hdr_cells[1].text = 'Action'
        hdr_cells[2].text = 'Parameters'
        hdr_cells[3].text = 'UUID'
        hdr_cells[4].text = 'User'
        hdr_cells[5].text = 'IP Address'
        #hdr_cells[6].text = 'IP Port'

        # Add a row for each record
        for record in records:
            row_cells = table.add_row().cells
            row_cells[0].text = str(record.date)
            row_cells[1].text = str(record.action)
            row_cells[2].text = str(record.parameters)
            row_cells[3].text = str(record.uuid)
            row_cells[4].text = str(record.user.username)
            row_cells[5].text = str(record.ip_address)
            #row_cells[6].text = str(record.ip_port)

            # Change font size to 8 pt
            for cell in row_cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        run.font.size = Pt(8)

        # Save to BytesIO
        f = io.BytesIO()
        doc.save(f)
        f.seek(0)

        # Return as a Word document
        response = HttpResponse(
            f.read(),
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        response['Content-Disposition'] = 'inline; filename=chain_of_custody.docx'
        return response


@method_decorator(csrf_exempt, name='dispatch')
class RecordCommentView(View):
    """
    API View that handles POST requests to record a comment on the chain of custody.

    This view requires an API key for authentication. If the API key is valid
    and is associated with an active user, the comment will be recorded.

    If the API key is missing, invalid, or associated with an inactive user, an error message is returned.

    The expected format of the POST request:
    {
        "comment": "Your comment here...",
        "uuid": "example-uuid"
    }
    """

    authentication_classes = [SessionAuthentication]
    permission_classes = []

    def post(self, request):
        """
        Handles the POST request to record a comment on the chain of custody.

        Args:
            request: The HTTP request from the client. Expected to contain the API key in the headers 
            and the comment and uuid in the body.

        Returns:
            JsonResponse: A JsonResponse that either confirms the comment was recorded or returns an error message.
        """

        user, api_key_error = self.get_user_or_key_error(request)
        if api_key_error:
            return api_key_error

        # Get comment and uuid from request body
        try:
            body = json.loads(request.body)
            comment = body.get('comment')
            uuid = body.get('uuid')
            if not comment or not uuid:
                return JsonResponse({'error': 'Both comment and uuid are required'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid request format'}, status=400)

        # Record the comment on the chain of custody
        sync_create_chain_of_custody_record(request, "Chain of Custody Comment", comment, uuid)

        return JsonResponse({'message': 'Comment recorded successfully'}, status=200)

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


recordings = {}

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
        sync_create_chain_of_custody_record(request, "Download video", filename, uuid)
        
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

video_writers = {}


async def create_video(uuid, output_video_path):
    """
    Asynchronously create a video from screenshots taken in a virtual machine using QEMU Machine Protocol (QMP).

    The function connects to QMP, executes a screendump command to take a screenshot and saves it to a specified path.
    It then reads the screenshot into an image and writes the image as a frame to a video file.
    If the video writer is not yet set up, it initializes it with the size of the first frame.
    Once the frame has been written to the video, it removes the screenshot file.

    Parameters:
    ----------
    uuid : str
        The unique identifier for the video file's directory.
    output_video_path : str
        The path where the output video will be saved.

    Raises:
    ------
    Exception
        Any exception that occurs while creating the video or connecting/disconnecting from QMP.
    """
    qmp = QMPClient('forensicVM')
    socket_path = f"/forensicVM/mnt/vm/{uuid}/run/qmp.sock"
    frame_path = f"/forensicVM/mnt/vm/{uuid}/frames"
    screenshot_path = f"/forensicVM/mnt/vm/{uuid}/frames/screenshot.ppm"

    if not os.path.exists(frame_path):
        os.makedirs(frame_path)

    try:
        await qmp.connect(socket_path)
        res = await qmp.execute('screendump', {"filename": screenshot_path})

        # Load screenshot as an image
        img = cv2.imread(screenshot_path)

        # If the video writer is not yet set up, initialize it with the size of the first frame
        if uuid not in video_writers:
            height, width, _ = img.shape
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video_writers[uuid] = cv2.VideoWriter(output_video_path, fourcc, 25, (width, height))
            print("Video writer defined")

        # Write frame to video
        video_writers[uuid].write(img)


        # Remove screenshot
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)
    except Exception as e:
        print(e)
    finally:
        await qmp.disconnect()



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
                await async_create_chain_of_custody_record(request, "Start video recording", f"video{video_count + 1:04d}.mp4", uuid)

                for _ in range(3600*3):  # run the loop for 3600 interactions*3 (three hour)
                    await asyncio.sleep(1)  # sleep for 1 second
                    if not recordings[uuid]:  # if recordings[uuid] is False, break the loop
                        break

                scheduler.remove_job(f'create_video_job_{uuid}')
                if uuid in video_writers:
                    video_writers[uuid].release()
                    del video_writers[uuid]  # remove the VideoWriter from the dictionary


                result = {'video_recorded': True, 'message': f'Video recorded with the name video{video_count + 1:04d}.mp4'}
                await async_create_chain_of_custody_record(request, "Stop video recording", f"video{video_count + 1:04d}.mp4", uuid)
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
            # Set the user in the request object
            request.user = user
            await async_create_chain_of_custody_record(request, "Remove datetime", "", uuid)
            return JsonResponse({'message': f'Date time line removed successfully for VM {uuid}'}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': f'Error updating VM date time: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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

            request.user = user
            await async_create_chain_of_custody_record(request, "Set datetime", f"{datetime_str}", uuid)
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
        request.user = user
        await async_create_chain_of_custody_record(request, "Download pcap network traffic", "pcap.zip", uuid)

        return response



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

        request.user = user
        await async_create_chain_of_custody_record(request, "Enabled network card", "", uuid)
        return JsonResponse({'message': f'Tap interface {tap_interface} started successfully'}, status=status.HTTP_200_OK)

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

        request.user = user
        await async_create_chain_of_custody_record(request, "Disabled network card", "", uuid)
        return JsonResponse({'message': f'Tap interface {tap_interface} stopped successfully'}, status=status.HTTP_200_OK)


def get_available_memory():
    """
    Get the current available system memory.

    This function uses the psutil library to fetch system memory information.
    It returns the amount of available memory in Megabytes.

    Returns:
    -------
    float
        The amount of available system memory in Megabytes.
    """
    mem_info = psutil.virtual_memory()
    available_memory = mem_info.available / 1024 / 1024  # Convert to MB
    return available_memory

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

            request.user = user
            sync_create_chain_of_custody_record(request, "Changed memory size", f"{new_memory_size}", uuid)

            return JsonResponse({'message': 'Memory size updated successfully'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid or missing memory_size parameter'}, status=400)


#@method_decorator(csrf_exempt, name='dispatch')
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

async def delete_snapshot(uuid, snapshot_name):
    """
    Asynchronously delete a snapshot of a specific VM.

    This function uses QEMU's QMP (QEMU Machine Protocol) to execute commands on the VM.
    It specifically runs the `delvm` command to delete the snapshot.

    Args:
        uuid (str): The unique identifier for the VM.
        snapshot_name (str): The name of the snapshot to delete.

    Returns:
        str: A message indicating whether the snapshot was successfully deleted or not.
    """
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

        request.user = user
        await async_create_chain_of_custody_record(request, "Deleted snapshot", f"{snapshot_name}", uuid)

        return JsonResponse({'message': delete_status}, status=200)


async def rollback_snapshot(uuid, snapshot_name):
    """
    Asynchronously rollback to a snapshot of a specific VM.

    This function uses QEMU's QMP (QEMU Machine Protocol) to execute commands on the VM.
    It specifically runs the `loadvm` command to rollback to the snapshot.

    Args:
        uuid (str): The unique identifier for the VM.
        snapshot_name (str): The name of the snapshot to rollback to.

    Returns:
        str: A message indicating whether the snapshot was successfully rolled back or not.
    """
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

async def rollback_golden_snapshot(uuid):
    """
    Asynchronously rollback to the golden snapshot of a specific VM.


    Args:
        uuid (str): The unique identifier for the VM.

    Returns:
        str: A message indicating whether the snapshot was successfully rolled back or not.
    """
    try:
        command = "sudo /usr/bin/qemu-img snapshot -a goldenSnapshot /forensicVM/mnt/vm/" + uuid + "/S0002-P0001.qcow2-sda"
        result = await subprocess.run(command, shell=True, check=True)
        if result.returncode >0:
            raise Exception("Could not rollback golden snapshot")
        return "Snapshot rollback successful."
    except Exception as e:
        print(e)
        return "Error rolling back snapshot."


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
        request.user = user
        await async_create_chain_of_custody_record(request, "Rollback snapshot", f"{snapshot_name}", uuid)
        return JsonResponse({'message': rollback_status}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class RollbackGoldenSnapshotView(View):
    """
    API View that handles POST requests to rollback the golden snapshot of a specific VM.

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

        rollback_status = await rollback_golden_snapshot(uuid)
        request.user = user
        await async_create_chain_of_custody_record(request, "Rollback to initial state", f"Golden snapshot used to rollback to initial state", uuid)
        return JsonResponse({'message': rollback_status}, status=200)



async def create_snapshot(uuid):
    """
    Asynchronously creates a snapshot of a specific VM.

    This function uses QEMU's QMP (QEMU Machine Protocol) to execute commands on the VM.
    It specifically runs the `savevm` command to create the snapshot.

    Args:
        uuid (str): The unique identifier for the VM.

    Returns:
        str: The name of the snapshot if successful, or an error message if an exception occurred.
    """
    qmp = QMPClient('forensicVM')
    socket_path = f"/forensicVM/mnt/vm/{uuid}/run/qmp.sock"

    print(socket_path)
    try:
        await qmp.connect(socket_path)

        res = await qmp.execute('query-status')
        print(res)
        print(f"VM status: {res['status']}")
        status = res['status']

        snapshot_name = datetime.now().strftime("snap-%Y-%m-%d_%H%M%S")

        print(snapshot_name)

        res = await qmp.execute("human-monitor-command", {
            "command-line": f"savevm {snapshot_name}"
        })

        print(f"Snapshot '{snapshot_name}' created.")

        return snapshot_name
    except Exception as e:
        print(e)
        return "Error creating snapshot."
    finally:
        await qmp.disconnect()


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
        request.user = user
        await async_create_chain_of_custody_record(request, "Create snapshot", f"{snapshot_name}", uuid)
        return JsonResponse({'snapshot_name': snapshot_name}, status=200)

async def get_snapshots(uuid):
    """
    Asynchronously retrieves the list of snapshots of a specific VM.

    This function uses QEMU's QMP (QEMU Machine Protocol) to execute commands on the VM.
    It specifically runs the `info snapshots` command to retrieve the list of snapshots.

    Args:
        uuid (str): The unique identifier for the VM.

    Returns:
        list: A list of dictionaries containing snapshot information. Each dictionary includes
              snapshot id, tag, VM size, date, and VM clock.
              If an exception occurred, an empty list is returned.
    """
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


def create_and_format_qcow2(qcow2_file, folders):
    """
    Creates and formats a new QCOW2 file with a capacity of 20GB, and initializes it with a new NTFS partition.

    This function first creates a new QCOW2 file using the `qemu-img` command. Then, it initializes a new NTFS partition on
    the QCOW2 file using the `guestfish` command-line tool.

    After the partition is created, the function creates a series of folders in the root directory of the partition.
    Finally, it writes a readme file in the root directory of the partition.

    Args:
        qcow2_file (str): The path where the new QCOW2 file will be created.
        folders (list): A list of folder names that will be created in the root directory of the NTFS partition.

    Raises:
        subprocess.CalledProcessError: If the `qemu-img` command or the `guestfish` command fails.
    """
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

            request.user = user
            sync_create_chain_of_custody_record(request, "Run plugin", f"{plugin_directory}", image_uuid)

            return JsonResponse({'output': output}, status=status.HTTP_200_OK)
        except subprocess.CalledProcessError as e:
            return JsonResponse({'error': f'Plugin execution failed: {e.stderr}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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


def get_plugin_info(plugin_dir, info):
    """
    Runs the 'info' command of the plugin script and retrieves the specified information.

    Parameters:
    plugin_dir (str): The directory where the plugin script is located.
    info (str): The type of information to retrieve (e.g. 'plugin_name', 'plugin_description').

    Returns:
    str: The requested information, or an empty string if the information could not be retrieved.
    """
    run_script_path = os.path.join('/forensicVM/plugins', plugin_dir, 'run.sh')
    result = subprocess.run(['bash', run_script_path, 'info'], capture_output=True, text=True)
    output = result.stdout.strip()

    try:
        info_dict = json.loads(output)
    except json.JSONDecodeError:
        info_dict = {}

    return info_dict.get(info, '')

async def insert_network_card(uuid, mac_address=None):
    """
    Asynchronously inserts a network card into a specified virtual machine.

    This function first generates a random MAC address if none is provided. It then establishes a connection to
    the QEMU Machine Protocol (QMP) and sends commands to add a new network device to the machine.

    Parameters:
    uuid (str): The unique identifier of the virtual machine.
    mac_address (str, optional): The MAC address to assign to the network card.

    Returns:
    str: A confirmation message.
    """
    if not mac_address:
        # Generate a random MAC address if not supplied
        mac_address = generate_random_mac_address()

    qmp = QMPClient('forensicVM')
    socket_path = f"/forensicVM/mnt/vm/{uuid}/run/qmp.sock"

    try:
        await qmp.connect(socket_path)

        res = await qmp.execute("netdev_add",
                                { "type": "user",
                                  "id": "net0"})
        res = await qmp.execute("device_add",
                                { "driver": "virtio-net-pci",
                                  "netdev": "net0"})
        res = await qmp.execute("query-pci", {})
        print(res)

        print(f"Network card inserted with MAC address: {mac_address}")
    except Exception as e:
        print(e)
    finally:
        await qmp.disconnect()

    return "Network card inserted."

def generate_random_mac_address():
    """
    Generates a random MAC address.

    This function creates a MAC address with the locally administered and unicast bits set,
    and with the rest of the bits randomized.

    Returns:
    str: The generated MAC address.
    """
    import random

    mac = [0x52, 0x54, 0x00,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]

    mac_address = ':'.join(map(lambda x: "%02x" % x, mac))
    return mac_address

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


async def insert_cdrom(uuid, filename):
    """
    Asynchronously inserts a CD-ROM into a specified virtual machine.

    This function establishes a connection to the QEMU Machine Protocol (QMP) and sends a command to change the medium
    of the CD-ROM drive to the specified ISO file.

    Parameters:
    uuid (str): The unique identifier of the virtual machine.
    filename (str): The name of the ISO file to insert into the CD-ROM drive.

    Returns:
    str: A confirmation message.
    """
    qmp = QMPClient('forensicVM')
    socket_path = f"/forensicVM/mnt/vm/{uuid}/run/qmp.sock"


    try:
        await qmp.connect(socket_path)
        res = await qmp.execute("blockdev-change-medium",
                                { "id": "ide1-0-0",
                                  "filename": f"/forensicVM/mnt/iso/{filename}",
                                  "format": "raw" })
        print(f"CD-ROM inserted.")
    except Exception as e:
        print(e)
    finally:
        await qmp.disconnect()

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
        request.user = user
        await async_create_chain_of_custody_record(request, "Insert cdrom", f"{filename}", uuid)

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

async def eject_cdrom(uuid):
    """
    Asynchronously ejects the CD-ROM from a specified virtual machine.

    This function establishes a connection to the QEMU Machine Protocol (QMP) and sends a command to open the tray
    of the CD-ROM drive, effectively ejecting the CD-ROM.

    Parameters:
    uuid (str): The unique identifier of the virtual machine.

    Returns:
    str: A confirmation message.
    """
    qmp = QMPClient('forensicVM')
    socket_path = f"/forensicVM/mnt/vm/{uuid}/run/qmp.sock"


    try:
        await qmp.connect(socket_path)
        res = await qmp.execute("blockdev-open-tray",
                                { "id": "ide1-0-0"})
        print(f"CD-ROM ejected.")
    except Exception as e:
        print(e)
    finally:
        await qmp.disconnect()

    try:
        await qmp.connect(socket_path)
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
        request.user = user
        await async_create_chain_of_custody_record(request, "Eject cdrom", "", uuid)
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

        request.user = user
        sync_create_chain_of_custody_record(request, "Deleted cdrom", f"{filename}", "---")
        return JsonResponse({'message': f'ISO file {filename} deleted successfully'}, status=status.HTTP_200_OK)


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

        request.user = user
        sync_create_chain_of_custody_record(request, "Upload cdrom", f"{iso_file.name}", "---")
        return JsonResponse({'message': 'ISO file uploaded successfully'}, status=status.HTTP_200_OK)


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


def change_qcow2(qcow2_file, folders):
    """
    This function creates new folders in a qcow2 disk image. It uses guestfish commands to interact with the disk image.

    Parameters:
    qcow2_file (str): Path to the qcow2 file that should be changed.
    folders (list): List of folder names to be created in the qcow2 image.

    Returns:
    None

    Raises:
    subprocess.CalledProcessError: If a guestfish command fails.
    """
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
        request.user = user
        await async_create_chain_of_custody_record(request, "Download evidence drive", "evidence.vmdk", uuid)
        return response

async def memory_snapshot(uuid):
    """
    This asynchronous function captures a snapshot of a VM's memory.

    It establishes a connection with the QEMU Machine Protocol (QMP) running on the VM,
    then uses the QMP command 'dump-guest-memory' to capture the memory snapshot.

    The function saves the memory snapshot to the VM's directory, with a unique filename
    based on the current number of existing snapshots.

    Parameters:
    uuid (str): The UUID of the VM.

    Returns:
    str: The path to the newly created memory snapshot file.

    Raises:
    Exception: If there's an error executing the 'dump-guest-memory' command or disconnecting from QMP.
    """
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
        request.user = user
        await async_create_chain_of_custody_record(request, "Make and download memory dump", "memory.dump", uuid)
        return response

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
        request.user = user
        await async_create_chain_of_custody_record(request, "Download screenshots", "screenshots.zip", uuid)
        return response

async def screendump(uuid):
    """
    Capture a screenshot of a Virtual Machine (VM) and save it as a PNG file.

    This function uses the QEMU Machine Protocol (QMP) to communicate with the VM and issue the 'screendump' command,
    which captures a screenshot of the current state of the VM's display. The screenshot is saved to a directory
    named 'screenshots' within the VM's directory, and the file is named 'sc' followed by a five-digit number,
    with leading zeroes as necessary.

    Args:
        uuid: The UUID of the VM to capture a screenshot from.

    Returns:
        The number of the screenshot that was taken, as an integer.

    Raises:
        Prints an exception error if the QMP connection or command execution fails.
    """
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
        return(next_screenshot_number)
    except Exception as e:
        print(e)
    finally:
        await qmp.disconnect()

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
        request.user = user
        await async_create_chain_of_custody_record(request, "Make screenshot", f"{screen_number}", uuid)
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


async def system_shutdown(uuid):
    """
    This function sends a shutdown command to a VM specified by its UUID. It uses QEMU's QMP (QEMU Machine Protocol)
    to interact with the VM.

    Args:
        uuid (str): The UUID of the VM to be shutdown.

    Raises:
        Exception: If there's an error while trying to interact with the VM, an exception will be raised.
    """
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
        request.user = user
        await async_create_chain_of_custody_record(request, "Sent Shutdown", "", uuid)
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


async def system_reset(uuid):
    """
    This function sends a reset command to a VM specified by its UUID. It uses QEMU's QMP (QEMU Machine Protocol)
    to interact with the VM.

    Args:
        uuid (str): The UUID of the VM to be reset.

    Raises:
        Exception: If there's an error while trying to interact with the VM, an exception will be raised.
    """
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
        request.user = user
        await async_create_chain_of_custody_record(request, "Sent Reset", "", uuid)
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
            request.user = user
            sync_create_chain_of_custody_record(request, "DELETED VM", "", uuid)
        except Exception as e:
            result = {'vm_deleted': False, 'error': str(e)}

        return Response(result, status=status.HTTP_200_OK)

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

def find_available_port(start_port):
    """
    This function finds two available, sequential TCP ports to use, starting from the given `start_port`.

    Args:
        start_port (int): The port number from which to start checking for availability.

    Returns:
        tuple: A pair of two available, sequential TCP port numbers.

    Raises:
        OSError: If an error occurs that is not related to a port being in use (e.g., permission denied, etc.)
    """
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
        request.user = user
        sync_create_chain_of_custody_record(request, "Stopped VM", "", uuid)
        return Response(result, status=status.HTTP_200_OK)


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

        request.user = user
        sync_create_chain_of_custody_record(request, "Started VM", "", uuid)
        return Response(result, status=status.HTTP_200_OK)

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
        mode_file = os.path.join(vm_path, "mode")

        #if not os.path.exists(mode_file):
        if not os.path.exists(vm_path):
            print("Does no exist")
            return Response({'PATH': 'not_exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            result = {'PATH': 'exists'}

            mode = None
            if os.path.exists(mode_file):
                with open(mode_file, 'r') as f:
                    mode = f.read().strip()
            result['running_mode'] = mode

            if os.path.exists(pid_file):
                with open(pid_file, 'r') as f:
                    pid = f.read().strip()

                cmd = f"ps -ef | grep {pid} | grep {uuid}"
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                output, _ = process.communicate()

                if output:
                    result['vm_status'] = 'running'


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
            request.user = user
            sync_create_chain_of_custody_record(request, "Tried to copy to server the user ssh keys", "", "")
            return Response({'message': 'Public key already added to authorized keys'}, status=status.HTTP_200_OK)

        # Add public key to authorized keys of the forensicinvestigator user
        try:
            with open(authorized_keys_file, 'a') as f:
                f.write(public_key + '\n')
        except FileNotFoundError:
            return Response({'error': 'Failed to append public key to authorized keys file'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        request.user = user
        sync_create_chain_of_custody_record(request, "Created new ssh keys for user om the server", "", "")
        return Response({'message': 'Public key added to authorized keys'}, status=status.HTTP_200_OK)


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
