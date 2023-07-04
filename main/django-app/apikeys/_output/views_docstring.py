def basename(p):
    """Returns the final component of a pathname"""
    p = os.fspath(p)
    sep = _get_sep(p)
    i = p.rfind(sep) + 1
    return p[i:]
    """Returns the final component of a pathname"""

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
    """This function creates new folders in a qcow2 disk image. It uses guestfish commands to interact with the disk image.

Parameters:
qcow2_file (str): Path to the qcow2 file that should be changed.
folders (list): List of folder names to be created in the qcow2 image.

Returns:
None

Raises:
subprocess.CalledProcessError: If a guestfish command fails."""

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
    """Creates and formats a new QCOW2 file with a capacity of 20GB, and initializes it with a new NTFS partition.

This function first creates a new QCOW2 file using the `qemu-img` command. Then, it initializes a new NTFS partition on
the QCOW2 file using the `guestfish` command-line tool.

After the partition is created, the function creates a series of folders in the root directory of the partition.
Finally, it writes a readme file in the root directory of the partition.

Args:
    qcow2_file (str): The path where the new QCOW2 file will be created.
    folders (list): A list of folder names that will be created in the root directory of the NTFS partition.

Raises:
    subprocess.CalledProcessError: If the `qemu-img` command or the `guestfish` command fails."""

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
    """Asynchronously creates a snapshot of a specific VM.

This function uses QEMU's QMP (QEMU Machine Protocol) to execute commands on the VM.
It specifically runs the `savevm` command to create the snapshot.

Args:
    uuid (str): The unique identifier for the VM.

Returns:
    str: The name of the snapshot if successful, or an error message if an exception occurred."""

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
    """Asynchronously create a video from screenshots taken in a virtual machine using QEMU Machine Protocol (QMP).

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
    Any exception that occurs while creating the video or connecting/disconnecting from QMP."""

def csrf_exempt(view_func):
    """Mark a view function as being exempt from the CSRF view protection."""

    # view_func.csrf_exempt = True would also work, but decorators are nicer
    # if they don't have side effects, so return a new function.
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)

    wrapped_view.csrf_exempt = True
    return wraps(view_func)(wrapped_view)
    """Mark a view function as being exempt from the CSRF view protection."""

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
    """Asynchronously delete a snapshot of a specific VM.

This function uses QEMU's QMP (QEMU Machine Protocol) to execute commands on the VM.
It specifically runs the `delvm` command to delete the snapshot.

Args:
    uuid (str): The unique identifier for the VM.
    snapshot_name (str): The name of the snapshot to delete.

Returns:
    str: A message indicating whether the snapshot was successfully deleted or not."""

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
                                { "id": "ide0-0-0"})
        print(f"CD-ROM ejected.")
    except Exception as e:
        print(e)
    finally:
        await qmp.disconnect()

    return "CD-ROM ejected."
    """Asynchronously ejects the CD-ROM from a specified virtual machine.

This function establishes a connection to the QEMU Machine Protocol (QMP) and sends a command to open the tray
of the CD-ROM drive, effectively ejecting the CD-ROM.

Parameters:
uuid (str): The unique identifier of the virtual machine.

Returns:
str: A confirmation message."""

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
    """This function finds two available, sequential TCP ports to use, starting from the given `start_port`.

Args:
    start_port (int): The port number from which to start checking for availability.

Returns:
    tuple: A pair of two available, sequential TCP port numbers.

Raises:
    OSError: If an error occurs that is not related to a port being in use (e.g., permission denied, etc.)"""

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
    """Generates a random MAC address.

This function creates a MAC address with the locally administered and unicast bits set,
and with the rest of the bits randomized.

Returns:
str: The generated MAC address."""

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
    """Get the current available system memory.

This function uses the psutil library to fetch system memory information.
It returns the amount of available memory in Megabytes.

Returns:
-------
float
    The amount of available system memory in Megabytes."""

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
    """Runs the 'info' command of the plugin script and retrieves the specified information.

Parameters:
plugin_dir (str): The directory where the plugin script is located.
info (str): The type of information to retrieve (e.g. 'plugin_name', 'plugin_description').

Returns:
str: The requested information, or an empty string if the information could not be retrieved."""

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
    """Asynchronously retrieves the list of snapshots of a specific VM.

This function uses QEMU's QMP (QEMU Machine Protocol) to execute commands on the VM.
It specifically runs the `info snapshots` command to retrieve the list of snapshots.

Args:
    uuid (str): The unique identifier for the VM.

Returns:
    list: A list of dictionaries containing snapshot information. Each dictionary includes
          snapshot id, tag, VM size, date, and VM clock.
          If an exception occurred, an empty list is returned."""

def get_user(request):
    """
    Return the user model instance associated with the given request session.
    If no user is retrieved, return an instance of `AnonymousUser`.
    """
    from .models import AnonymousUser

    user = None
    try:
        user_id = _get_user_session_key(request)
        backend_path = request.session[BACKEND_SESSION_KEY]
    except KeyError:
        pass
    else:
        if backend_path in settings.AUTHENTICATION_BACKENDS:
            backend = load_backend(backend_path)
            user = backend.get_user(user_id)
            # Verify the session
            if hasattr(user, "get_session_auth_hash"):
                session_hash = request.session.get(HASH_SESSION_KEY)
                if not session_hash:
                    session_hash_verified = False
                else:
                    session_auth_hash = user.get_session_auth_hash()
                    session_hash_verified = constant_time_compare(
                        session_hash, session_auth_hash
                    )
                if not session_hash_verified:
                    # If the current secret does not verify the session, try
                    # with the fallback secrets and stop when a matching one is
                    # found.
                    if session_hash and any(
                        constant_time_compare(session_hash, fallback_auth_hash)
                        for fallback_auth_hash in user.get_session_auth_fallback_hash()
                    ):
                        request.session.cycle_key()
                        request.session[HASH_SESSION_KEY] = session_auth_hash
                    else:
                        request.session.flush()
                        user = None

    return user or AnonymousUser()
    """Return the user model instance associated with the given request session.
If no user is retrieved, return an instance of `AnonymousUser`."""

def get_user_model():
    """
    Return the User model that is active in this project.
    """
    try:
        return django_apps.get_model(settings.AUTH_USER_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            "AUTH_USER_MODEL must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            "AUTH_USER_MODEL refers to model '%s' that has not been installed"
            % settings.AUTH_USER_MODEL
        )
    """Return the User model that is active in this project."""

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
                                { "id": "ide0-0-0",
                                  "filename": f"/forensicVM/mnt/iso/{filename}",
                                  "format": "raw" })
        print(f"CD-ROM inserted.")
    except Exception as e:
        print(e)
    finally:
        await qmp.disconnect()

    return "CD-ROM inserted."
    """Asynchronously inserts a CD-ROM into a specified virtual machine.

This function establishes a connection to the QEMU Machine Protocol (QMP) and sends a command to change the medium
of the CD-ROM drive to the specified ISO file.

Parameters:
uuid (str): The unique identifier of the virtual machine.
filename (str): The name of the ISO file to insert into the CD-ROM drive.

Returns:
str: A confirmation message."""

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
    """Asynchronously inserts a network card into a specified virtual machine.

This function first generates a random MAC address if none is provided. It then establishes a connection to
the QEMU Machine Protocol (QMP) and sends commands to add a new network device to the machine.

Parameters:
uuid (str): The unique identifier of the virtual machine.
mac_address (str, optional): The MAC address to assign to the network card.

Returns:
str: A confirmation message."""

def isfile(path):
    """Test whether a path is a regular file"""
    try:
        st = os.stat(path)
    except (OSError, ValueError):
        return False
    return stat.S_ISREG(st.st_mode)
    """Test whether a path is a regular file"""

def join(a, *p):
    """Join two or more pathname components, inserting '/' as needed.
    If any component is an absolute path, all previous path components
    will be discarded.  An empty last part will result in a path that
    ends with a separator."""
    a = os.fspath(a)
    sep = _get_sep(a)
    path = a
    try:
        if not p:
            path[:0] + sep  #23780: Ensure compatible data type even if p is null.
        for b in map(os.fspath, p):
            if b.startswith(sep):
                path = b
            elif not path or path.endswith(sep):
                path += b
            else:
                path += sep + b
    except (TypeError, AttributeError, BytesWarning):
        genericpath._check_arg_types('join', a, *p)
        raise
    return path
    """Join two or more pathname components, inserting '/' as needed.
If any component is an absolute path, all previous path components
will be discarded.  An empty last part will result in a path that
ends with a separator."""

def login_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None
):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
    """Decorator for views that checks that the user is logged in, redirecting
to the log-in page if necessary."""

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
    """This asynchronous function captures a snapshot of a VM's memory.

It establishes a connection with the QEMU Machine Protocol (QMP) running on the VM,
then uses the QMP command 'dump-guest-memory' to capture the memory snapshot.

The function saves the memory snapshot to the VM's directory, with a unique filename
based on the current number of existing snapshots.

Parameters:
uuid (str): The UUID of the VM.

Returns:
str: The path to the newly created memory snapshot file.

Raises:
Exception: If there's an error executing the 'dump-guest-memory' command or disconnecting from QMP."""

def method_decorator(decorator, name=""):
    """
    Convert a function decorator into a method decorator
    """

    # 'obj' can be a class or a function. If 'obj' is a function at the time it
    # is passed to _dec,  it will eventually be a method of the class it is
    # defined on. If 'obj' is a class, the 'name' is required to be the name
    # of the method that will be decorated.
    def _dec(obj):
        if not isinstance(obj, type):
            return _multi_decorate(decorator, obj)
        if not (name and hasattr(obj, name)):
            raise ValueError(
                "The keyword argument `name` must be the name of a method "
                "of the decorated class: %s. Got '%s' instead." % (obj, name)
            )
        method = getattr(obj, name)
        if not callable(method):
            raise TypeError(
                "Cannot decorate '%s' as it isn't a callable attribute of "
                "%s (%s)." % (name, obj, method)
            )
        _wrapper = _multi_decorate(decorator, method)
        setattr(obj, name, _wrapper)
        return obj

    # Don't worry about making _dec look similar to a list/tuple as it's rather
    # meaningless.
    if not hasattr(decorator, "__iter__"):
        update_wrapper(_dec, decorator)
    # Change the name to aid debugging.
    obj = decorator if hasattr(decorator, "__name__") else decorator.__class__
    _dec.__name__ = "method_decorator(%s)" % obj.__name__
    return _dec
    """Convert a function decorator into a method decorator"""

def quote(string, safe='/', encoding=None, errors=None):
    """quote('abc def') -> 'abc%20def'

    Each part of a URL, e.g. the path info, the query, etc., has a
    different set of reserved characters that must be quoted. The
    quote function offers a cautious (not minimal) way to quote a
    string for most of these parts.

    RFC 3986 Uniform Resource Identifier (URI): Generic Syntax lists
    the following (un)reserved characters.

    unreserved    = ALPHA / DIGIT / "-" / "." / "_" / "~"
    reserved      = gen-delims / sub-delims
    gen-delims    = ":" / "/" / "?" / "#" / "[" / "]" / "@"
    sub-delims    = "!" / "$" / "&" / "'" / "(" / ")"
                  / "*" / "+" / "," / ";" / "="

    Each of the reserved characters is reserved in some component of a URL,
    but not necessarily in all of them.

    The quote function %-escapes all characters that are neither in the
    unreserved chars ("always safe") nor the additional chars set via the
    safe arg.

    The default for the safe arg is '/'. The character is reserved, but in
    typical usage the quote function is being called on a path where the
    existing slash characters are to be preserved.

    Python 3.7 updates from using RFC 2396 to RFC 3986 to quote URL strings.
    Now, "~" is included in the set of unreserved characters.

    string and safe may be either str or bytes objects. encoding and errors
    must not be specified if string is a bytes object.

    The optional encoding and errors parameters specify how to deal with
    non-ASCII characters, as accepted by the str.encode method.
    By default, encoding='utf-8' (characters are encoded with UTF-8), and
    errors='strict' (unsupported characters raise a UnicodeEncodeError).
    """
    if isinstance(string, str):
        if not string:
            return string
        if encoding is None:
            encoding = 'utf-8'
        if errors is None:
            errors = 'strict'
        string = string.encode(encoding, errors)
    else:
        if encoding is not None:
            raise TypeError("quote() doesn't support 'encoding' for bytes")
        if errors is not None:
            raise TypeError("quote() doesn't support 'errors' for bytes")
    return quote_from_bytes(string, safe)
    """quote('abc def') -> 'abc%20def'

Each part of a URL, e.g. the path info, the query, etc., has a
different set of reserved characters that must be quoted. The
quote function offers a cautious (not minimal) way to quote a
string for most of these parts.

RFC 3986 Uniform Resource Identifier (URI): Generic Syntax lists
the following (un)reserved characters.

unreserved    = ALPHA / DIGIT / "-" / "." / "_" / "~"
reserved      = gen-delims / sub-delims
gen-delims    = ":" / "/" / "?" / "#" / "[" / "]" / "@"
sub-delims    = "!" / "$" / "&" / "'" / "(" / ")"
              / "*" / "+" / "," / ";" / "="

Each of the reserved characters is reserved in some component of a URL,
but not necessarily in all of them.

The quote function %-escapes all characters that are neither in the
unreserved chars ("always safe") nor the additional chars set via the
safe arg.

The default for the safe arg is '/'. The character is reserved, but in
typical usage the quote function is being called on a path where the
existing slash characters are to be preserved.

Python 3.7 updates from using RFC 2396 to RFC 3986 to quote URL strings.
Now, "~" is included in the set of unreserved characters.

string and safe may be either str or bytes objects. encoding and errors
must not be specified if string is a bytes object.

The optional encoding and errors parameters specify how to deal with
non-ASCII characters, as accepted by the str.encode method.
By default, encoding='utf-8' (characters are encoded with UTF-8), and
errors='strict' (unsupported characters raise a UnicodeEncodeError)."""

def render(
    request, template_name, context=None, content_type=None, status=None, using=None
):
    """
    Return an HttpResponse whose content is filled with the result of calling
    django.template.loader.render_to_string() with the passed arguments.
    """
    content = loader.render_to_string(template_name, context, request, using=using)
    return HttpResponse(content, content_type, status)
    """Return an HttpResponse whose content is filled with the result of calling
django.template.loader.render_to_string() with the passed arguments."""

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
    """Asynchronously rollback to a snapshot of a specific VM.

This function uses QEMU's QMP (QEMU Machine Protocol) to execute commands on the VM.
It specifically runs the `loadvm` command to rollback to the snapshot.

Args:
    uuid (str): The unique identifier for the VM.
    snapshot_name (str): The name of the snapshot to rollback to.

Returns:
    str: A message indicating whether the snapshot was successfully rolled back or not."""

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
    """Capture a screenshot of a Virtual Machine (VM) and save it as a PNG file.

This function uses the QEMU Machine Protocol (QMP) to communicate with the VM and issue the 'screendump' command,
which captures a screenshot of the current state of the VM's display. The screenshot is saved to a directory
named 'screenshots' within the VM's directory, and the file is named 'sc' followed by a five-digit number,
with leading zeroes as necessary.

Args:
    uuid: The UUID of the VM to capture a screenshot from.

Returns:
    The number of the screenshot that was taken, as an integer.

Raises:
    Prints an exception error if the QMP connection or command execution fails."""

def sync_to_async(
    func=None,
    thread_sensitive=True,
    executor=None,
):
    if func is None:
        return lambda f: SyncToAsync(
            f,
            thread_sensitive=thread_sensitive,
            executor=executor,
        )
    return SyncToAsync(
        func,
        thread_sensitive=thread_sensitive,
        executor=executor,
    )

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
    """This function sends a reset command to a VM specified by its UUID. It uses QEMU's QMP (QEMU Machine Protocol)
to interact with the VM.

Args:
    uuid (str): The UUID of the VM to be reset.

Raises:
    Exception: If there's an error while trying to interact with the VM, an exception will be raised."""

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
    """This function sends a shutdown command to a VM specified by its UUID. It uses QEMU's QMP (QEMU Machine Protocol)
to interact with the VM.

Args:
    uuid (str): The UUID of the VM to be shutdown.

Raises:
    Exception: If there's an error while trying to interact with the VM, an exception will be raised."""

def validate_date(date_str):
    """
    Function to validate the date string against the format 'YYYY-MM-DDTHH:MM:SS'
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
        return True
    except ValueError:
        return False
    """Function to validate the date string against the format 'YYYY-MM-DDTHH:MM:SS'"""

class APIView(View):

    # The following policies may be set at either globally, or per-view.
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    parser_classes = api_settings.DEFAULT_PARSER_CLASSES
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    throttle_classes = api_settings.DEFAULT_THROTTLE_CLASSES
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES
    content_negotiation_class = api_settings.DEFAULT_CONTENT_NEGOTIATION_CLASS
    metadata_class = api_settings.DEFAULT_METADATA_CLASS
    versioning_class = api_settings.DEFAULT_VERSIONING_CLASS

    # Allow dependency injection of other settings to make testing easier.
    settings = api_settings

    schema = DefaultSchema()

    @classmethod
    def as_view(cls, **initkwargs):
        """
        Store the original class on the view function.

        This allows us to discover information about the view when we do URL
        reverse lookups.  Used for breadcrumb generation.
        """
        if isinstance(getattr(cls, 'queryset', None), models.query.QuerySet):
            def force_evaluation():
                raise RuntimeError(
                    'Do not evaluate the `.queryset` attribute directly, '
                    'as the result will be cached and reused between requests. '
                    'Use `.all()` or call `.get_queryset()` instead.'
                )
            cls.queryset._fetch_all = force_evaluation

        view = super().as_view(**initkwargs)
        view.cls = cls
        view.initkwargs = initkwargs

        # Note: session based authentication is explicitly CSRF validated,
        # all other authentication is CSRF exempt.
        return csrf_exempt(view)

    @property
    def allowed_methods(self):
        """
        Wrap Django's private `_allowed_methods` interface in a public property.
        """
        return self._allowed_methods()

    @property
    def default_response_headers(self):
        headers = {
            'Allow': ', '.join(self.allowed_methods),
        }
        if len(self.renderer_classes) > 1:
            headers['Vary'] = 'Accept'
        return headers

    def http_method_not_allowed(self, request, *args, **kwargs):
        """
        If `request.method` does not correspond to a handler method,
        determine what kind of exception to raise.
        """
        raise exceptions.MethodNotAllowed(request.method)

    def permission_denied(self, request, message=None, code=None):
        """
        If request is not permitted, determine what kind of exception to raise.
        """
        if request.authenticators and not request.successful_authenticator:
            raise exceptions.NotAuthenticated()
        raise exceptions.PermissionDenied(detail=message, code=code)

    def throttled(self, request, wait):
        """
        If request is throttled, determine what kind of exception to raise.
        """
        raise exceptions.Throttled(wait)

    def get_authenticate_header(self, request):
        """
        If a request is unauthenticated, determine the WWW-Authenticate
        header to use for 401 responses, if any.
        """
        authenticators = self.get_authenticators()
        if authenticators:
            return authenticators[0].authenticate_header(request)

    def get_parser_context(self, http_request):
        """
        Returns a dict that is passed through to Parser.parse(),
        as the `parser_context` keyword argument.
        """
        # Note: Additionally `request` and `encoding` will also be added
        #       to the context by the Request object.
        return {
            'view': self,
            'args': getattr(self, 'args', ()),
            'kwargs': getattr(self, 'kwargs', {})
        }

    def get_renderer_context(self):
        """
        Returns a dict that is passed through to Renderer.render(),
        as the `renderer_context` keyword argument.
        """
        # Note: Additionally 'response' will also be added to the context,
        #       by the Response object.
        return {
            'view': self,
            'args': getattr(self, 'args', ()),
            'kwargs': getattr(self, 'kwargs', {}),
            'request': getattr(self, 'request', None)
        }

    def get_exception_handler_context(self):
        """
        Returns a dict that is passed through to EXCEPTION_HANDLER,
        as the `context` argument.
        """
        return {
            'view': self,
            'args': getattr(self, 'args', ()),
            'kwargs': getattr(self, 'kwargs', {}),
            'request': getattr(self, 'request', None)
        }

    def get_view_name(self):
        """
        Return the view name, as used in OPTIONS responses and in the
        browsable API.
        """
        func = self.settings.VIEW_NAME_FUNCTION
        return func(self)

    def get_view_description(self, html=False):
        """
        Return some descriptive text for the view, as used in OPTIONS responses
        and in the browsable API.
        """
        func = self.settings.VIEW_DESCRIPTION_FUNCTION
        return func(self, html)

    # API policy instantiation methods

    def get_format_suffix(self, **kwargs):
        """
        Determine if the request includes a '.json' style format suffix
        """
        if self.settings.FORMAT_SUFFIX_KWARG:
            return kwargs.get(self.settings.FORMAT_SUFFIX_KWARG)

    def get_renderers(self):
        """
        Instantiates and returns the list of renderers that this view can use.
        """
        return [renderer() for renderer in self.renderer_classes]

    def get_parsers(self):
        """
        Instantiates and returns the list of parsers that this view can use.
        """
        return [parser() for parser in self.parser_classes]

    def get_authenticators(self):
        """
        Instantiates and returns the list of authenticators that this view can use.
        """
        return [auth() for auth in self.authentication_classes]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        return [permission() for permission in self.permission_classes]

    def get_throttles(self):
        """
        Instantiates and returns the list of throttles that this view uses.
        """
        return [throttle() for throttle in self.throttle_classes]

    def get_content_negotiator(self):
        """
        Instantiate and return the content negotiation class to use.
        """
        if not getattr(self, '_negotiator', None):
            self._negotiator = self.content_negotiation_class()
        return self._negotiator

    def get_exception_handler(self):
        """
        Returns the exception handler that this view uses.
        """
        return self.settings.EXCEPTION_HANDLER

    # API policy implementation methods

    def perform_content_negotiation(self, request, force=False):
        """
        Determine which renderer and media type to use render the response.
        """
        renderers = self.get_renderers()
        conneg = self.get_content_negotiator()

        try:
            return conneg.select_renderer(request, renderers, self.format_kwarg)
        except Exception:
            if force:
                return (renderers[0], renderers[0].media_type)
            raise

    def perform_authentication(self, request):
        """
        Perform authentication on the incoming request.

        Note that if you override this and simply 'pass', then authentication
        will instead be performed lazily, the first time either
        `request.user` or `request.auth` is accessed.
        """
        request.user

    def check_permissions(self, request):
        """
        Check if the request should be permitted.
        Raises an appropriate exception if the request is not permitted.
        """
        for permission in self.get_permissions():
            if not permission.has_permission(request, self):
                self.permission_denied(
                    request,
                    message=getattr(permission, 'message', None),
                    code=getattr(permission, 'code', None)
                )

    def check_object_permissions(self, request, obj):
        """
        Check if the request should be permitted for a given object.
        Raises an appropriate exception if the request is not permitted.
        """
        for permission in self.get_permissions():
            if not permission.has_object_permission(request, self, obj):
                self.permission_denied(
                    request,
                    message=getattr(permission, 'message', None),
                    code=getattr(permission, 'code', None)
                )

    def check_throttles(self, request):
        """
        Check if request should be throttled.
        Raises an appropriate exception if the request is throttled.
        """
        throttle_durations = []
        for throttle in self.get_throttles():
            if not throttle.allow_request(request, self):
                throttle_durations.append(throttle.wait())

        if throttle_durations:
            # Filter out `None` values which may happen in case of config / rate
            # changes, see #1438
            durations = [
                duration for duration in throttle_durations
                if duration is not None
            ]

            duration = max(durations, default=None)
            self.throttled(request, duration)

    def determine_version(self, request, *args, **kwargs):
        """
        If versioning is being used, then determine any API version for the
        incoming request. Returns a two-tuple of (version, versioning_scheme)
        """
        if self.versioning_class is None:
            return (None, None)
        scheme = self.versioning_class()
        return (scheme.determine_version(request, *args, **kwargs), scheme)

    # Dispatch methods

    def initialize_request(self, request, *args, **kwargs):
        """
        Returns the initial request object.
        """
        parser_context = self.get_parser_context(request)

        return Request(
            request,
            parsers=self.get_parsers(),
            authenticators=self.get_authenticators(),
            negotiator=self.get_content_negotiator(),
            parser_context=parser_context
        )

    def initial(self, request, *args, **kwargs):
        """
        Runs anything that needs to occur prior to calling the method handler.
        """
        self.format_kwarg = self.get_format_suffix(**kwargs)

        # Perform content negotiation and store the accepted info on the request
        neg = self.perform_content_negotiation(request)
        request.accepted_renderer, request.accepted_media_type = neg

        # Determine the API version, if versioning is in use.
        version, scheme = self.determine_version(request, *args, **kwargs)
        request.version, request.versioning_scheme = version, scheme

        # Ensure that the incoming request is permitted
        self.perform_authentication(request)
        self.check_permissions(request)
        self.check_throttles(request)

    def finalize_response(self, request, response, *args, **kwargs):
        """
        Returns the final response object.
        """
        # Make the error obvious if a proper response is not returned
        assert isinstance(response, HttpResponseBase), (
            'Expected a `Response`, `HttpResponse` or `HttpStreamingResponse` '
            'to be returned from the view, but received a `%s`'
            % type(response)
        )

        if isinstance(response, Response):
            if not getattr(request, 'accepted_renderer', None):
                neg = self.perform_content_negotiation(request, force=True)
                request.accepted_renderer, request.accepted_media_type = neg

            response.accepted_renderer = request.accepted_renderer
            response.accepted_media_type = request.accepted_media_type
            response.renderer_context = self.get_renderer_context()

        # Add new vary headers to the response instead of overwriting.
        vary_headers = self.headers.pop('Vary', None)
        if vary_headers is not None:
            patch_vary_headers(response, cc_delim_re.split(vary_headers))

        for key, value in self.headers.items():
            response[key] = value

        return response

    def handle_exception(self, exc):
        """
        Handle any exception that occurs, by returning an appropriate response,
        or re-raising the error.
        """
        if isinstance(exc, (exceptions.NotAuthenticated,
                            exceptions.AuthenticationFailed)):
            # WWW-Authenticate header for 401 responses, else coerce to 403
            auth_header = self.get_authenticate_header(self.request)

            if auth_header:
                exc.auth_header = auth_header
            else:
                exc.status_code = status.HTTP_403_FORBIDDEN

        exception_handler = self.get_exception_handler()

        context = self.get_exception_handler_context()
        response = exception_handler(exc, context)

        if response is None:
            self.raise_uncaught_exception(exc)

        response.exception = True
        return response

    def raise_uncaught_exception(self, exc):
        if settings.DEBUG:
            request = self.request
            renderer_format = getattr(request.accepted_renderer, 'format')
            use_plaintext_traceback = renderer_format not in ('html', 'api', 'admin')
            request.force_plaintext_errors(use_plaintext_traceback)
        raise exc

    # Note: Views are made CSRF exempt from within `as_view` as to prevent
    # accidental removal of this exemption in cases where `dispatch` needs to
    # be overridden.
    def dispatch(self, request, *args, **kwargs):
        """
        `.dispatch()` is pretty much the same as Django's regular dispatch,
        but with extra hooks for startup, finalize, and exception handling.
        """
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            self.initial(request, *args, **kwargs)

            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response

    def options(self, request, *args, **kwargs):
        """
        Handler method for HTTP 'OPTIONS' request.
        """
        if self.metadata_class is None:
            return self.http_method_not_allowed(request, *args, **kwargs)
        data = self.metadata_class().determine_metadata(request, self)
        return Response(data, status=status.HTTP_200_OK)
    """Intentionally simple parent class for all views. Only implements
dispatch-by-method and simple sanity checking."""

class ApiKey(models.Model):
    """Model representing an API key associated with a user."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def mask_key(self):
        """Return a masked version of the API key."""
        masked_key_length = 4
        if self.key is None:
            masked_key = 'N/A'
        else:
            masked_key = '*' * (len(str(self.key)) - masked_key_length)
            masked_key += str(self.key)[-masked_key_length:]
        return masked_key

    def __str__(self):
        """Return the masked version of the API key when the instance is converted to a string."""
        return self.mask_key()
    """Model representing an API key associated with a user."""

class AsyncIOScheduler(BaseScheduler):
    """
    A scheduler that runs on an asyncio (:pep:`3156`) event loop.

    The default executor can run jobs based on native coroutines (``async def``).

    Extra options:

    ============== =============================================================
    ``event_loop`` AsyncIO event loop to use (defaults to the global event loop)
    ============== =============================================================
    """

    _eventloop = None
    _timeout = None

    def start(self, paused=False):
        if not self._eventloop:
            self._eventloop = asyncio.get_event_loop()

        super(AsyncIOScheduler, self).start(paused)

    @run_in_event_loop
    def shutdown(self, wait=True):
        super(AsyncIOScheduler, self).shutdown(wait)
        self._stop_timer()

    def _configure(self, config):
        self._eventloop = maybe_ref(config.pop('event_loop', None))
        super(AsyncIOScheduler, self)._configure(config)

    def _start_timer(self, wait_seconds):
        self._stop_timer()
        if wait_seconds is not None:
            self._timeout = self._eventloop.call_later(wait_seconds, self.wakeup)

    def _stop_timer(self):
        if self._timeout:
            self._timeout.cancel()
            del self._timeout

    @run_in_event_loop
    def wakeup(self):
        self._stop_timer()
        wait_seconds = self._process_jobs()
        self._start_timer(wait_seconds)

    def _create_default_executor(self):
        from apscheduler.executors.asyncio import AsyncIOExecutor
        return AsyncIOExecutor()
    """A scheduler that runs on an asyncio (:pep:`3156`) event loop.

The default executor can run jobs based on native coroutines (``async def``).

Extra options:

============== =============================================================
``event_loop`` AsyncIO event loop to use (defaults to the global event loop)
============== ============================================================="""

class CalledProcessError(SubprocessError):
    """Raised when run() is called with check=True and the process
    returns a non-zero exit status.

    Attributes:
      cmd, returncode, stdout, stderr, output
    """
    def __init__(self, returncode, cmd, output=None, stderr=None):
        self.returncode = returncode
        self.cmd = cmd
        self.output = output
        self.stderr = stderr

    def __str__(self):
        if self.returncode and self.returncode < 0:
            try:
                return "Command '%s' died with %r." % (
                        self.cmd, signal.Signals(-self.returncode))
            except ValueError:
                return "Command '%s' died with unknown signal %d." % (
                        self.cmd, -self.returncode)
        else:
            return "Command '%s' returned non-zero exit status %d." % (
                    self.cmd, self.returncode)

    @property
    def stdout(self):
        """Alias for output attribute, to match stderr"""
        return self.output

    @stdout.setter
    def stdout(self, value):
        # There's no obvious reason to set this, but allow it anyway so
        # .stdout is a transparent alias for .output
        self.output = value
    """Raised when run() is called with check=True and the process
returns a non-zero exit status.

Attributes:
  cmd, returncode, stdout, stderr, output"""

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

class FileResponse(StreamingHttpResponse):
    """
    A streaming HTTP response class optimized for files.
    """

    block_size = 4096

    def __init__(self, *args, as_attachment=False, filename="", **kwargs):
        self.as_attachment = as_attachment
        self.filename = filename
        self._no_explicit_content_type = (
            "content_type" not in kwargs or kwargs["content_type"] is None
        )
        super().__init__(*args, **kwargs)

    def _set_streaming_content(self, value):
        if not hasattr(value, "read"):
            self.file_to_stream = None
            return super()._set_streaming_content(value)

        self.file_to_stream = filelike = value
        if hasattr(filelike, "close"):
            self._resource_closers.append(filelike.close)
        value = iter(lambda: filelike.read(self.block_size), b"")
        self.set_headers(filelike)
        super()._set_streaming_content(value)

    def set_headers(self, filelike):
        """
        Set some common response headers (Content-Length, Content-Type, and
        Content-Disposition) based on the `filelike` response content.
        """
        filename = getattr(filelike, "name", "")
        filename = filename if isinstance(filename, str) else ""
        seekable = hasattr(filelike, "seek") and (
            not hasattr(filelike, "seekable") or filelike.seekable()
        )
        if hasattr(filelike, "tell"):
            if seekable:
                initial_position = filelike.tell()
                filelike.seek(0, io.SEEK_END)
                self.headers["Content-Length"] = filelike.tell() - initial_position
                filelike.seek(initial_position)
            elif hasattr(filelike, "getbuffer"):
                self.headers["Content-Length"] = (
                    filelike.getbuffer().nbytes - filelike.tell()
                )
            elif os.path.exists(filename):
                self.headers["Content-Length"] = (
                    os.path.getsize(filename) - filelike.tell()
                )
        elif seekable:
            self.headers["Content-Length"] = sum(
                iter(lambda: len(filelike.read(self.block_size)), 0)
            )
            filelike.seek(-int(self.headers["Content-Length"]), io.SEEK_END)

        filename = os.path.basename(self.filename or filename)
        if self._no_explicit_content_type:
            if filename:
                content_type, encoding = mimetypes.guess_type(filename)
                # Encoding isn't set to prevent browsers from automatically
                # uncompressing files.
                content_type = {
                    "bzip2": "application/x-bzip",
                    "gzip": "application/gzip",
                    "xz": "application/x-xz",
                }.get(encoding, content_type)
                self.headers["Content-Type"] = (
                    content_type or "application/octet-stream"
                )
            else:
                self.headers["Content-Type"] = "application/octet-stream"

        if filename:
            disposition = "attachment" if self.as_attachment else "inline"
            try:
                filename.encode("ascii")
                file_expr = 'filename="{}"'.format(
                    filename.replace("\\", "\\\\").replace('"', r"\"")
                )
            except UnicodeEncodeError:
                file_expr = "filename*=utf-8''{}".format(quote(filename))
            self.headers["Content-Disposition"] = "{}; {}".format(
                disposition, file_expr
            )
        elif self.as_attachment:
            self.headers["Content-Disposition"] = "attachment"
    """A streaming HTTP response class optimized for files."""

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

class Http404(Exception):
    pass
    """Common base class for all non-exit exceptions."""

class HttpResponseBadRequest(HttpResponse):
    status_code = 400
    """An HTTP response class with a string as content.

This content can be read, appended to, or replaced."""

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

class JsonResponse(HttpResponse):
    """
    An HTTP response class that consumes data to be serialized to JSON.

    :param data: Data to be dumped into json. By default only ``dict`` objects
      are allowed to be passed due to a security flaw before ECMAScript 5. See
      the ``safe`` parameter for more information.
    :param encoder: Should be a json encoder class. Defaults to
      ``django.core.serializers.json.DjangoJSONEncoder``.
    :param safe: Controls if only ``dict`` objects may be serialized. Defaults
      to ``True``.
    :param json_dumps_params: A dictionary of kwargs passed to json.dumps().
    """

    def __init__(
        self,
        data,
        encoder=DjangoJSONEncoder,
        safe=True,
        json_dumps_params=None,
        **kwargs,
    ):
        if safe and not isinstance(data, dict):
            raise TypeError(
                "In order to allow non-dict objects to be serialized set the "
                "safe parameter to False."
            )
        if json_dumps_params is None:
            json_dumps_params = {}
        kwargs.setdefault("content_type", "application/json")
        data = json.dumps(data, cls=encoder, **json_dumps_params)
        super().__init__(content=data, **kwargs)
    """An HTTP response class that consumes data to be serialized to JSON.

:param data: Data to be dumped into json. By default only ``dict`` objects
  are allowed to be passed due to a security flaw before ECMAScript 5. See
  the ``safe`` parameter for more information.
:param encoder: Should be a json encoder class. Defaults to
  ``django.core.serializers.json.DjangoJSONEncoder``.
:param safe: Controls if only ``dict`` objects may be serialized. Defaults
  to ``True``.
:param json_dumps_params: A dictionary of kwargs passed to json.dumps()."""

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

class QMPClient(AsyncProtocol[Message], Events):
    """Implements a QMP client connection.

    `QMPClient` can be used to either connect or listen to a QMP server,
    but always acts as the QMP client.

    :param name:
        Optional nickname for the connection, used to differentiate
        instances when logging.

    Basic script-style usage looks like this::

      import asyncio
      from qemu.qmp import QMPClient

      async def main():
          qmp = QMPClient('my_virtual_machine_name')
          await qmp.connect(('127.0.0.1', 1234))
          ...
          res = await qmp.execute('query-block')
          ...
          await qmp.disconnect()

      asyncio.run(main())

    A more advanced example that starts to take advantage of asyncio
    might look like this::

      class Client:
          def __init__(self, name: str):
              self.qmp = QMPClient(name)

          async def watch_events(self):
              try:
                  async for event in self.qmp.events:
                      print(f"Event: {event['event']}")
              except asyncio.CancelledError:
                  return

          async def run(self, address='/tmp/qemu.socket'):
              await self.qmp.connect(address)
              asyncio.create_task(self.watch_events())
              await self.qmp.runstate_changed.wait()
              await self.disconnect()

    See `qmp.events` for more detail on event handling patterns.

    """
    #: Logger object used for debugging messages.
    logger = logging.getLogger(__name__)

    # Read buffer limit; large enough to accept query-qmp-schema
    _limit = (256 * 1024)

    # Type alias for pending execute() result items
    _PendingT = Union[Message, ExecInterruptedError]

    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__(name)
        Events.__init__(self)

        #: Whether or not to await a greeting after establishing a connection.
        #: Defaults to True; QGA servers expect this to be False.
        self.await_greeting: bool = True

        #: Whether or not to perform capabilities negotiation upon
        #: connection. Implies `await_greeting`. Defaults to True; QGA
        #: servers expect this to be False.
        self.negotiate: bool = True

        # Cached Greeting, if one was awaited.
        self._greeting: Optional[Greeting] = None

        # Command ID counter
        self._execute_id = 0

        # Incoming RPC reply messages.
        self._pending: Dict[
            Union[str, None],
            'asyncio.Queue[QMPClient._PendingT]'
        ] = {}

    @property
    def greeting(self) -> Optional[Greeting]:
        """
        The `Greeting` from the QMP server, if any.

        Defaults to ``None``, and will be set after a greeting is
        received during the connection process. It is reset at the start
        of each connection attempt.
        """
        return self._greeting

    @upper_half
    async def _establish_session(self) -> None:
        """
        Initiate the QMP session.

        Wait for the QMP greeting and perform capabilities negotiation.

        :raise GreetingError: When the greeting is not understood.
        :raise NegotiationError: If the negotiation fails.
        :raise EOFError: When the server unexpectedly hangs up.
        :raise OSError: For underlying stream errors.
        """
        self._greeting = None
        self._pending = {}

        if self.await_greeting or self.negotiate:
            self._greeting = await self._get_greeting()

        if self.negotiate:
            await self._negotiate()

        # This will start the reader/writers:
        await super()._establish_session()

    @upper_half
    async def _get_greeting(self) -> Greeting:
        """
        :raise GreetingError: When the greeting is not understood.
        :raise EOFError: When the server unexpectedly hangs up.
        :raise OSError: For underlying stream errors.

        :return: the Greeting object given by the server.
        """
        self.logger.debug("Awaiting greeting ...")

        try:
            msg = await self._recv()
            return Greeting(msg)
        except (ProtocolError, KeyError, TypeError) as err:
            emsg = "Did not understand Greeting"
            self.logger.error("%s: %s", emsg, exception_summary(err))
            self.logger.debug("%s:\n%s\n", emsg, pretty_traceback())
            raise GreetingError(emsg, err) from err
        except BaseException as err:
            # EOFError, OSError, or something unexpected.
            emsg = "Failed to receive Greeting"
            self.logger.error("%s: %s", emsg, exception_summary(err))
            self.logger.debug("%s:\n%s\n", emsg, pretty_traceback())
            raise

    @upper_half
    async def _negotiate(self) -> None:
        """
        Perform QMP capabilities negotiation.

        :raise NegotiationError: When negotiation fails.
        :raise EOFError: When the server unexpectedly hangs up.
        :raise OSError: For underlying stream errors.
        """
        self.logger.debug("Negotiating capabilities ...")

        arguments: Dict[str, List[str]] = {}
        if self._greeting and 'oob' in self._greeting.QMP.capabilities:
            arguments.setdefault('enable', []).append('oob')
        msg = self.make_execute_msg('qmp_capabilities', arguments=arguments)

        # It's not safe to use execute() here, because the reader/writers
        # aren't running. AsyncProtocol *requires* that a new session
        # does not fail after the reader/writers are running!
        try:
            await self._send(msg)
            reply = await self._recv()
            assert 'return' in reply
            assert 'error' not in reply
        except (ProtocolError, AssertionError) as err:
            emsg = "Negotiation failed"
            self.logger.error("%s: %s", emsg, exception_summary(err))
            self.logger.debug("%s:\n%s\n", emsg, pretty_traceback())
            raise NegotiationError(emsg, err) from err
        except BaseException as err:
            # EOFError, OSError, or something unexpected.
            emsg = "Negotiation failed"
            self.logger.error("%s: %s", emsg, exception_summary(err))
            self.logger.debug("%s:\n%s\n", emsg, pretty_traceback())
            raise

    @bottom_half
    async def _bh_disconnect(self) -> None:
        try:
            await super()._bh_disconnect()
        finally:
            if self._pending:
                self.logger.debug("Cancelling pending executions")
            keys = self._pending.keys()
            for key in keys:
                self.logger.debug("Cancelling execution '%s'", key)
                self._pending[key].put_nowait(
                    ExecInterruptedError("Disconnected")
                )

            self.logger.debug("QMP Disconnected.")

    @upper_half
    def _cleanup(self) -> None:
        super()._cleanup()
        assert not self._pending

    @bottom_half
    async def _on_message(self, msg: Message) -> None:
        """
        Add an incoming message to the appropriate queue/handler.

        :raise ServerParseError: When Message indicates server parse failure.
        """
        # Incoming messages are not fully parsed/validated here;
        # do only light peeking to know how to route the messages.

        if 'event' in msg:
            await self._event_dispatch(msg)
            return

        # Below, we assume everything left is an execute/exec-oob response.

        exec_id = cast(Optional[str], msg.get('id'))

        if exec_id in self._pending:
            await self._pending[exec_id].put(msg)
            return

        # We have a message we can't route back to a caller.

        is_error = 'error' in msg
        has_id = 'id' in msg

        if is_error and not has_id:
            # This is very likely a server parsing error.
            # It doesn't inherently belong to any pending execution.
            # Instead of performing clever recovery, just terminate.
            # See "NOTE" in qmp-spec.txt, section 2.4.2
            raise ServerParseError(
                ("Server sent an error response without an ID, "
                 "but there are no ID-less executions pending. "
                 "Assuming this is a server parser failure."),
                msg
            )

        # qmp-spec.txt, section 2.4:
        # 'Clients should drop all the responses
        # that have an unknown "id" field.'
        self.logger.log(
            logging.ERROR if is_error else logging.WARNING,
            "Unknown ID '%s', message dropped.",
            exec_id,
        )
        self.logger.debug("Unroutable message: %s", str(msg))

    @upper_half
    @bottom_half
    async def _do_recv(self) -> Message:
        """
        :raise OSError: When a stream error is encountered.
        :raise EOFError: When the stream is at EOF.
        :raise ProtocolError:
            When the Message is not understood.
            See also `Message._deserialize`.

        :return: A single QMP `Message`.
        """
        msg_bytes = await self._readline()
        msg = Message(msg_bytes, eager=True)
        return msg

    @upper_half
    @bottom_half
    def _do_send(self, msg: Message) -> None:
        """
        :raise ValueError: JSON serialization failure
        :raise TypeError: JSON serialization failure
        :raise OSError: When a stream error is encountered.
        """
        assert self._writer is not None
        self._writer.write(bytes(msg))

    @upper_half
    def _get_exec_id(self) -> str:
        exec_id = f"__qmp#{self._execute_id:05d}"
        self._execute_id += 1
        return exec_id

    @upper_half
    async def _issue(self, msg: Message) -> Union[None, str]:
        """
        Issue a QMP `Message` and do not wait for a reply.

        :param msg: The QMP `Message` to send to the server.

        :return: The ID of the `Message` sent.
        """
        msg_id: Optional[str] = None
        if 'id' in msg:
            assert isinstance(msg['id'], str)
            msg_id = msg['id']

        self._pending[msg_id] = asyncio.Queue(maxsize=1)
        try:
            await self._outgoing.put(msg)
        except:
            del self._pending[msg_id]
            raise

        return msg_id

    @upper_half
    async def _reply(self, msg_id: Union[str, None]) -> Message:
        """
        Await a reply to a previously issued QMP message.

        :param msg_id: The ID of the previously issued message.

        :return: The reply from the server.
        :raise ExecInterruptedError:
            When the reply could not be retrieved because the connection
            was lost, or some other problem.
        """
        queue = self._pending[msg_id]

        try:
            result = await queue.get()
            if isinstance(result, ExecInterruptedError):
                raise result
            return result
        finally:
            del self._pending[msg_id]

    @upper_half
    async def _execute(self, msg: Message, assign_id: bool = True) -> Message:
        """
        Send a QMP `Message` to the server and await a reply.

        This method *assumes* you are sending some kind of an execute
        statement that *will* receive a reply.

        An execution ID will be assigned if assign_id is `True`. It can be
        disabled, but this requires that an ID is manually assigned
        instead. For manually assigned IDs, you must not use the string
        '__qmp#' anywhere in the ID.

        :param msg: The QMP `Message` to execute.
        :param assign_id: If True, assign a new execution ID.

        :return: Execution reply from the server.
        :raise ExecInterruptedError:
            When the reply could not be retrieved because the connection
            was lost, or some other problem.
        """
        if assign_id:
            msg['id'] = self._get_exec_id()
        elif 'id' in msg:
            assert isinstance(msg['id'], str)
            assert '__qmp#' not in msg['id']

        exec_id = await self._issue(msg)
        return await self._reply(exec_id)

    @upper_half
    @require(Runstate.RUNNING)
    async def _raw(
            self,
            msg: Union[Message, Mapping[str, object], bytes],
            assign_id: bool = True,
    ) -> Message:
        """
        Issue a raw `Message` to the QMP server and await a reply.

        :param msg:
            A Message to send to the server. It may be a `Message`, any
            Mapping (including Dict), or raw bytes.
        :param assign_id:
            Assign an arbitrary execution ID to this message. If
            `False`, the existing id must either be absent (and no other
            such pending execution may omit an ID) or a string. If it is
            a string, it must not start with '__qmp#' and no other such
            pending execution may currently be using that ID.

        :return: Execution reply from the server.

        :raise ExecInterruptedError:
            When the reply could not be retrieved because the connection
            was lost, or some other problem.
        :raise TypeError:
            When assign_id is `False`, an ID is given, and it is not a string.
        :raise ValueError:
            When assign_id is `False`, but the ID is not usable;
            Either because it starts with '__qmp#' or it is already in-use.
        """
        # 1. convert generic Mapping or bytes to a QMP Message
        # 2. copy Message objects so that we assign an ID only to the copy.
        msg = Message(msg)

        exec_id = msg.get('id')
        if not assign_id and 'id' in msg:
            if not isinstance(exec_id, str):
                raise TypeError(f"ID ('{exec_id}') must be a string.")
            if exec_id.startswith('__qmp#'):
                raise ValueError(
                    f"ID ('{exec_id}') must not start with '__qmp#'."
                )

        if not assign_id and exec_id in self._pending:
            raise ValueError(
                f"ID '{exec_id}' is in-use and cannot be used."
            )

        return await self._execute(msg, assign_id=assign_id)

    @upper_half
    @require(Runstate.RUNNING)
    async def execute_msg(self, msg: Message) -> object:
        """
        Execute a QMP command on the server and return its value.

        :param msg: The QMP `Message` to execute.

        :return:
            The command execution return value from the server. The type of
            object returned depends on the command that was issued,
            though most in QEMU return a `dict`.
        :raise ValueError:
            If the QMP `Message` does not have either the 'execute' or
            'exec-oob' fields set.
        :raise ExecuteError: When the server returns an error response.
        :raise ExecInterruptedError:
            If the connection was disrupted before
            receiving a reply from the server.
        """
        if not ('execute' in msg or 'exec-oob' in msg):
            raise ValueError("Requires 'execute' or 'exec-oob' message")

        # Copy the Message so that the ID assigned by _execute() is
        # local to this method; allowing the ID to be seen in raised
        # Exceptions but without modifying the caller's held copy.
        msg = Message(msg)
        reply = await self._execute(msg)

        if 'error' in reply:
            try:
                error_response = ErrorResponse(reply)
            except (KeyError, TypeError) as err:
                # Error response was malformed.
                raise BadReplyError(
                    "QMP error reply is malformed", reply, msg,
                ) from err

            raise ExecuteError(error_response, msg, reply)

        if 'return' not in reply:
            raise BadReplyError(
                "QMP reply is missing a 'error' or 'return' member",
                reply, msg,
            )

        return reply['return']

    @classmethod
    def make_execute_msg(cls, cmd: str,
                         arguments: Optional[Mapping[str, object]] = None,
                         oob: bool = False) -> Message:
        """
        Create an executable message to be sent by `execute_msg` later.

        :param cmd: QMP command name.
        :param arguments: Arguments (if any). Must be JSON-serializable.
        :param oob:
            If `True`, execute `"out of band"
            <https://gitlab.com/qemu-project/qemu/-/blob/master/docs/interop/qmp-spec.txt#L116>`_.

        :return: A QMP `Message` that can be executed with `execute_msg()`.
        """
        msg = Message({'exec-oob' if oob else 'execute': cmd})
        if arguments is not None:
            msg['arguments'] = arguments
        return msg

    @upper_half
    async def execute(self, cmd: str,
                      arguments: Optional[Mapping[str, object]] = None,
                      oob: bool = False) -> object:
        """
        Execute a QMP command on the server and return its value.

        :param cmd: QMP command name.
        :param arguments: Arguments (if any). Must be JSON-serializable.
        :param oob:
            If `True`, execute `"out of band"
            <https://gitlab.com/qemu-project/qemu/-/blob/master/docs/interop/qmp-spec.txt#L116>`_.

        :return:
            The command execution return value from the server. The type of
            object returned depends on the command that was issued,
            though most in QEMU return a `dict`.
        :raise ExecuteError: When the server returns an error response.
        :raise ExecInterruptedError:
            If the connection was disrupted before
            receiving a reply from the server.
        """
        msg = self.make_execute_msg(cmd, arguments, oob=oob)
        return await self.execute_msg(msg)

    @upper_half
    @require(Runstate.RUNNING)
    def send_fd_scm(self, fd: int) -> None:
        """Send a file descriptor to the remote via SCM_RIGHTS.

        This method does not close the file descriptor.

        :param fd: The file descriptor to send to QEMU.

        This is an advanced feature of QEMU where file descriptors can
        be passed from client to server. This is usually used as a
        security measure to isolate the QEMU process from being able to
        open its own files. See the QMP commands ``getfd`` and
        ``add-fd`` for more information.

        See `socket.socket.sendmsg` for more information on the Python
        implementation for sending file descriptors over a UNIX socket.
        """
        assert self._writer is not None
        sock = self._writer.transport.get_extra_info('socket')

        if sock.family != socket.AF_UNIX:
            raise QMPError("Sending file descriptors requires a UNIX socket.")

        if not hasattr(sock, 'sendmsg'):
            # We need to void the warranty sticker.
            # Access to sendmsg is scheduled for removal in Python 3.11.
            # Find the real backing socket to use it anyway.
            sock = sock._sock  # pylint: disable=protected-access

        sock.sendmsg(
            [b' '],
            [(socket.SOL_SOCKET, socket.SCM_RIGHTS, struct.pack('@i', fd))]
        )
    """Implements a QMP client connection.

`QMPClient` can be used to either connect or listen to a QMP server,
but always acts as the QMP client.

:param name:
    Optional nickname for the connection, used to differentiate
    instances when logging.

Basic script-style usage looks like this::

  import asyncio
  from qemu.qmp import QMPClient

  async def main():
      qmp = QMPClient('my_virtual_machine_name')
      await qmp.connect(('127.0.0.1', 1234))
      ...
      res = await qmp.execute('query-block')
      ...
      await qmp.disconnect()

  asyncio.run(main())

A more advanced example that starts to take advantage of asyncio
might look like this::

  class Client:
      def __init__(self, name: str):
          self.qmp = QMPClient(name)

      async def watch_events(self):
          try:
              async for event in self.qmp.events:
                  print(f"Event: {event['event']}")
          except asyncio.CancelledError:
              return

      async def run(self, address='/tmp/qemu.socket'):
          await self.qmp.connect(address)
          asyncio.create_task(self.watch_events())
          await self.qmp.runstate_changed.wait()
          await self.disconnect()

See `qmp.events` for more detail on event handling patterns."""

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

class Response(SimpleTemplateResponse):
    """
    An HttpResponse that allows its data to be rendered into
    arbitrary media types.
    """

    def __init__(self, data=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.

        Setting 'renderer' and 'media_type' will typically be deferred,
        For example being set automatically by the `APIView`.
        """
        super().__init__(None, status=status)

        if isinstance(data, Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)

        self.data = data
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in headers.items():
                self[name] = value

    @property
    def rendered_content(self):
        renderer = getattr(self, 'accepted_renderer', None)
        accepted_media_type = getattr(self, 'accepted_media_type', None)
        context = getattr(self, 'renderer_context', None)

        assert renderer, ".accepted_renderer not set on Response"
        assert accepted_media_type, ".accepted_media_type not set on Response"
        assert context is not None, ".renderer_context not set on Response"
        context['response'] = self

        media_type = renderer.media_type
        charset = renderer.charset
        content_type = self.content_type

        if content_type is None and charset is not None:
            content_type = "{}; charset={}".format(media_type, charset)
        elif content_type is None:
            content_type = media_type
        self['Content-Type'] = content_type

        ret = renderer.render(self.data, accepted_media_type, context)
        if isinstance(ret, str):
            assert charset, (
                'renderer returned unicode, and did not specify '
                'a charset value.'
            )
            return ret.encode(charset)

        if not ret:
            del self['Content-Type']

        return ret

    @property
    def status_text(self):
        """
        Returns reason text corresponding to our HTTP response status code.
        Provided for convenience.
        """
        return responses.get(self.status_code, '')

    def __getstate__(self):
        """
        Remove attributes from the response that shouldn't be cached.
        """
        state = super().__getstate__()
        for key in (
            'accepted_renderer', 'renderer_context', 'resolver_match',
            'client', 'request', 'json', 'wsgi_request'
        ):
            if key in state:
                del state[key]
        state['_closable_objects'] = []
        return state
    """An HttpResponse that allows its data to be rendered into
arbitrary media types."""

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

class SessionAuthentication(BaseAuthentication):
    """
    Use Django's session framework for authentication.
    """

    def authenticate(self, request):
        """
        Returns a `User` if the request session currently has a logged in user.
        Otherwise returns `None`.
        """

        # Get the session-based user from the underlying HttpRequest object
        user = getattr(request._request, 'user', None)

        # Unauthenticated, CSRF validation not required
        if not user or not user.is_active:
            return None

        self.enforce_csrf(request)

        # CSRF passed with authenticated user
        return (user, None)

    def enforce_csrf(self, request):
        """
        Enforce CSRF validation for session based authentication.
        """
        def dummy_get_response(request):  # pragma: no cover
            return None

        check = CSRFCheck(dummy_get_response)
        # populates request.META['CSRF_COOKIE'], which is used in process_view()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            # CSRF failed, bail with explicit error message
            raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)
    """Use Django's session framework for authentication."""

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

class AsyncToSync:
    """
    Utility class which turns an awaitable that only works on the thread with
    the event loop into a synchronous callable that works in a subthread.

    If the call stack contains an async loop, the code runs there.
    Otherwise, the code runs in a new loop in a new thread.

    Either way, this thread then pauses and waits to run any thread_sensitive
    code called from further down the call stack using SyncToAsync, before
    finally exiting once the async task returns.
    """

    # Maps launched Tasks to the threads that launched them (for locals impl)
    launch_map: "Dict[asyncio.Task[object], threading.Thread]" = {}

    # Keeps track of which CurrentThreadExecutor to use. This uses an asgiref
    # Local, not a threadlocal, so that tasks can work out what their parent used.
    executors = Local()

    # When we can't find a CurrentThreadExecutor from the context, such as
    # inside create_task, we'll look it up here from the running event loop.
    loop_thread_executors: "Dict[asyncio.AbstractEventLoop, CurrentThreadExecutor]" = {}

    def __init__(self, awaitable, force_new_loop=False):
        if not callable(awaitable) or (
            not _iscoroutinefunction_or_partial(awaitable)
            and not _iscoroutinefunction_or_partial(
                getattr(awaitable, "__call__", awaitable)
            )
        ):
            # Python does not have very reliable detection of async functions
            # (lots of false negatives) so this is just a warning.
            warnings.warn(
                "async_to_sync was passed a non-async-marked callable", stacklevel=2
            )
        self.awaitable = awaitable
        try:
            self.__self__ = self.awaitable.__self__
        except AttributeError:
            pass
        if force_new_loop:
            # They have asked that we always run in a new sub-loop.
            self.main_event_loop = None
        else:
            try:
                self.main_event_loop = asyncio.get_running_loop()
            except RuntimeError:
                # There's no event loop in this thread. Look for the threadlocal if
                # we're inside SyncToAsync
                main_event_loop_pid = getattr(
                    SyncToAsync.threadlocal, "main_event_loop_pid", None
                )
                # We make sure the parent loop is from the same process - if
                # they've forked, this is not going to be valid any more (#194)
                if main_event_loop_pid and main_event_loop_pid == os.getpid():
                    self.main_event_loop = getattr(
                        SyncToAsync.threadlocal, "main_event_loop", None
                    )
                else:
                    self.main_event_loop = None

    def __call__(self, *args, **kwargs):
        # You can't call AsyncToSync from a thread with a running event loop
        try:
            event_loop = asyncio.get_running_loop()
        except RuntimeError:
            pass
        else:
            if event_loop.is_running():
                raise RuntimeError(
                    "You cannot use AsyncToSync in the same thread as an async event loop - "
                    "just await the async function directly."
                )

        # Wrapping context in list so it can be reassigned from within
        # `main_wrap`.
        context = [contextvars.copy_context()]

        # Make a future for the return information
        call_result = Future()
        # Get the source thread
        source_thread = threading.current_thread()
        # Make a CurrentThreadExecutor we'll use to idle in this thread - we
        # need one for every sync frame, even if there's one above us in the
        # same thread.
        if hasattr(self.executors, "current"):
            old_current_executor = self.executors.current
        else:
            old_current_executor = None
        current_executor = CurrentThreadExecutor()
        self.executors.current = current_executor
        loop = None
        # Use call_soon_threadsafe to schedule a synchronous callback on the
        # main event loop's thread if it's there, otherwise make a new loop
        # in this thread.
        try:
            awaitable = self.main_wrap(
                args, kwargs, call_result, source_thread, sys.exc_info(), context
            )

            if not (self.main_event_loop and self.main_event_loop.is_running()):
                # Make our own event loop - in a new thread - and run inside that.
                loop = asyncio.new_event_loop()
                self.loop_thread_executors[loop] = current_executor
                loop_executor = ThreadPoolExecutor(max_workers=1)
                loop_future = loop_executor.submit(
                    self._run_event_loop, loop, awaitable
                )
                if current_executor:
                    # Run the CurrentThreadExecutor until the future is done
                    current_executor.run_until_future(loop_future)
                # Wait for future and/or allow for exception propagation
                loop_future.result()
            else:
                # Call it inside the existing loop
                self.main_event_loop.call_soon_threadsafe(
                    self.main_event_loop.create_task, awaitable
                )
                if current_executor:
                    # Run the CurrentThreadExecutor until the future is done
                    current_executor.run_until_future(call_result)
        finally:
            # Clean up any executor we were running
            if loop is not None:
                del self.loop_thread_executors[loop]
            if hasattr(self.executors, "current"):
                del self.executors.current
            if old_current_executor:
                self.executors.current = old_current_executor
            _restore_context(context[0])

        # Wait for results from the future.
        return call_result.result()

    def _run_event_loop(self, loop, coro):
        """
        Runs the given event loop (designed to be called in a thread).
        """
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(coro)
        finally:
            try:
                # mimic asyncio.run() behavior
                # cancel unexhausted async generators
                tasks = asyncio.all_tasks(loop)
                for task in tasks:
                    task.cancel()

                async def gather():
                    await asyncio.gather(*tasks, return_exceptions=True)

                loop.run_until_complete(gather())
                for task in tasks:
                    if task.cancelled():
                        continue
                    if task.exception() is not None:
                        loop.call_exception_handler(
                            {
                                "message": "unhandled exception during loop shutdown",
                                "exception": task.exception(),
                                "task": task,
                            }
                        )
                if hasattr(loop, "shutdown_asyncgens"):
                    loop.run_until_complete(loop.shutdown_asyncgens())
            finally:
                loop.close()
                asyncio.set_event_loop(self.main_event_loop)

    def __get__(self, parent, objtype):
        """
        Include self for methods
        """
        func = functools.partial(self.__call__, parent)
        return functools.update_wrapper(func, self.awaitable)

    async def main_wrap(
        self, args, kwargs, call_result, source_thread, exc_info, context
    ):
        """
        Wraps the awaitable with something that puts the result into the
        result/exception future.
        """
        if context is not None:
            _restore_context(context[0])

        current_task = SyncToAsync.get_current_task()
        self.launch_map[current_task] = source_thread
        try:
            # If we have an exception, run the function inside the except block
            # after raising it so exc_info is correctly populated.
            if exc_info[1]:
                try:
                    raise exc_info[1]
                except BaseException:
                    result = await self.awaitable(*args, **kwargs)
            else:
                result = await self.awaitable(*args, **kwargs)
        except BaseException as e:
            call_result.set_exception(e)
        else:
            call_result.set_result(result)
        finally:
            del self.launch_map[current_task]

            context[0] = contextvars.copy_context()
    """Utility class which turns an awaitable that only works on the thread with
the event loop into a synchronous callable that works in a subthread.

If the call stack contains an async loop, the code runs there.
Otherwise, the code runs in a new loop in a new thread.

Either way, this thread then pauses and waits to run any thread_sensitive
code called from further down the call stack using SyncToAsync, before
finally exiting once the async task returns."""

class datetime(date):
    """datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])

    The year, month and day arguments are required. tzinfo may be None, or an
    instance of a tzinfo subclass. The remaining arguments may be ints.
    """
    __slots__ = date.__slots__ + time.__slots__

    def __new__(cls, year, month=None, day=None, hour=0, minute=0, second=0,
                microsecond=0, tzinfo=None, *, fold=0):
        if (isinstance(year, (bytes, str)) and len(year) == 10 and
            1 <= ord(year[2:3])&0x7F <= 12):
            # Pickle support
            if isinstance(year, str):
                try:
                    year = bytes(year, 'latin1')
                except UnicodeEncodeError:
                    # More informative error message.
                    raise ValueError(
                        "Failed to encode latin1 string when unpickling "
                        "a datetime object. "
                        "pickle.load(data, encoding='latin1') is assumed.")
            self = object.__new__(cls)
            self.__setstate(year, month)
            self._hashcode = -1
            return self
        year, month, day = _check_date_fields(year, month, day)
        hour, minute, second, microsecond, fold = _check_time_fields(
            hour, minute, second, microsecond, fold)
        _check_tzinfo_arg(tzinfo)
        self = object.__new__(cls)
        self._year = year
        self._month = month
        self._day = day
        self._hour = hour
        self._minute = minute
        self._second = second
        self._microsecond = microsecond
        self._tzinfo = tzinfo
        self._hashcode = -1
        self._fold = fold
        return self

    # Read-only field accessors
    @property
    def hour(self):
        """hour (0-23)"""
        return self._hour

    @property
    def minute(self):
        """minute (0-59)"""
        return self._minute

    @property
    def second(self):
        """second (0-59)"""
        return self._second

    @property
    def microsecond(self):
        """microsecond (0-999999)"""
        return self._microsecond

    @property
    def tzinfo(self):
        """timezone info object"""
        return self._tzinfo

    @property
    def fold(self):
        return self._fold

    @classmethod
    def _fromtimestamp(cls, t, utc, tz):
        """Construct a datetime from a POSIX timestamp (like time.time()).

        A timezone info object may be passed in as well.
        """
        frac, t = _math.modf(t)
        us = round(frac * 1e6)
        if us >= 1000000:
            t += 1
            us -= 1000000
        elif us < 0:
            t -= 1
            us += 1000000

        converter = _time.gmtime if utc else _time.localtime
        y, m, d, hh, mm, ss, weekday, jday, dst = converter(t)
        ss = min(ss, 59)    # clamp out leap seconds if the platform has them
        result = cls(y, m, d, hh, mm, ss, us, tz)
        if tz is None:
            # As of version 2015f max fold in IANA database is
            # 23 hours at 1969-09-30 13:00:00 in Kwajalein.
            # Let's probe 24 hours in the past to detect a transition:
            max_fold_seconds = 24 * 3600

            # On Windows localtime_s throws an OSError for negative values,
            # thus we can't perform fold detection for values of time less
            # than the max time fold. See comments in _datetimemodule's
            # version of this method for more details.
            if t < max_fold_seconds and sys.platform.startswith("win"):
                return result

            y, m, d, hh, mm, ss = converter(t - max_fold_seconds)[:6]
            probe1 = cls(y, m, d, hh, mm, ss, us, tz)
            trans = result - probe1 - timedelta(0, max_fold_seconds)
            if trans.days < 0:
                y, m, d, hh, mm, ss = converter(t + trans // timedelta(0, 1))[:6]
                probe2 = cls(y, m, d, hh, mm, ss, us, tz)
                if probe2 == result:
                    result._fold = 1
        else:
            result = tz.fromutc(result)
        return result

    @classmethod
    def fromtimestamp(cls, t, tz=None):
        """Construct a datetime from a POSIX timestamp (like time.time()).

        A timezone info object may be passed in as well.
        """
        _check_tzinfo_arg(tz)

        return cls._fromtimestamp(t, tz is not None, tz)

    @classmethod
    def utcfromtimestamp(cls, t):
        """Construct a naive UTC datetime from a POSIX timestamp."""
        return cls._fromtimestamp(t, True, None)

    @classmethod
    def now(cls, tz=None):
        "Construct a datetime from time.time() and optional time zone info."
        t = _time.time()
        return cls.fromtimestamp(t, tz)

    @classmethod
    def utcnow(cls):
        "Construct a UTC datetime from time.time()."
        t = _time.time()
        return cls.utcfromtimestamp(t)

    @classmethod
    def combine(cls, date, time, tzinfo=True):
        "Construct a datetime from a given date and a given time."
        if not isinstance(date, _date_class):
            raise TypeError("date argument must be a date instance")
        if not isinstance(time, _time_class):
            raise TypeError("time argument must be a time instance")
        if tzinfo is True:
            tzinfo = time.tzinfo
        return cls(date.year, date.month, date.day,
                   time.hour, time.minute, time.second, time.microsecond,
                   tzinfo, fold=time.fold)

    @classmethod
    def fromisoformat(cls, date_string):
        """Construct a datetime from the output of datetime.isoformat()."""
        if not isinstance(date_string, str):
            raise TypeError('fromisoformat: argument must be str')

        # Split this at the separator
        dstr = date_string[0:10]
        tstr = date_string[11:]

        try:
            date_components = _parse_isoformat_date(dstr)
        except ValueError:
            raise ValueError(f'Invalid isoformat string: {date_string!r}')

        if tstr:
            try:
                time_components = _parse_isoformat_time(tstr)
            except ValueError:
                raise ValueError(f'Invalid isoformat string: {date_string!r}')
        else:
            time_components = [0, 0, 0, 0, None]

        return cls(*(date_components + time_components))

    def timetuple(self):
        "Return local time tuple compatible with time.localtime()."
        dst = self.dst()
        if dst is None:
            dst = -1
        elif dst:
            dst = 1
        else:
            dst = 0
        return _build_struct_time(self.year, self.month, self.day,
                                  self.hour, self.minute, self.second,
                                  dst)

    def _mktime(self):
        """Return integer POSIX timestamp."""
        epoch = datetime(1970, 1, 1)
        max_fold_seconds = 24 * 3600
        t = (self - epoch) // timedelta(0, 1)
        def local(u):
            y, m, d, hh, mm, ss = _time.localtime(u)[:6]
            return (datetime(y, m, d, hh, mm, ss) - epoch) // timedelta(0, 1)

        # Our goal is to solve t = local(u) for u.
        a = local(t) - t
        u1 = t - a
        t1 = local(u1)
        if t1 == t:
            # We found one solution, but it may not be the one we need.
            # Look for an earlier solution (if `fold` is 0), or a
            # later one (if `fold` is 1).
            u2 = u1 + (-max_fold_seconds, max_fold_seconds)[self.fold]
            b = local(u2) - u2
            if a == b:
                return u1
        else:
            b = t1 - u1
            assert a != b
        u2 = t - b
        t2 = local(u2)
        if t2 == t:
            return u2
        if t1 == t:
            return u1
        # We have found both offsets a and b, but neither t - a nor t - b is
        # a solution.  This means t is in the gap.
        return (max, min)[self.fold](u1, u2)


    def timestamp(self):
        "Return POSIX timestamp as float"
        if self._tzinfo is None:
            s = self._mktime()
            return s + self.microsecond / 1e6
        else:
            return (self - _EPOCH).total_seconds()

    def utctimetuple(self):
        "Return UTC time tuple compatible with time.gmtime()."
        offset = self.utcoffset()
        if offset:
            self -= offset
        y, m, d = self.year, self.month, self.day
        hh, mm, ss = self.hour, self.minute, self.second
        return _build_struct_time(y, m, d, hh, mm, ss, 0)

    def date(self):
        "Return the date part."
        return date(self._year, self._month, self._day)

    def time(self):
        "Return the time part, with tzinfo None."
        return time(self.hour, self.minute, self.second, self.microsecond, fold=self.fold)

    def timetz(self):
        "Return the time part, with same tzinfo."
        return time(self.hour, self.minute, self.second, self.microsecond,
                    self._tzinfo, fold=self.fold)

    def replace(self, year=None, month=None, day=None, hour=None,
                minute=None, second=None, microsecond=None, tzinfo=True,
                *, fold=None):
        """Return a new datetime with new values for the specified fields."""
        if year is None:
            year = self.year
        if month is None:
            month = self.month
        if day is None:
            day = self.day
        if hour is None:
            hour = self.hour
        if minute is None:
            minute = self.minute
        if second is None:
            second = self.second
        if microsecond is None:
            microsecond = self.microsecond
        if tzinfo is True:
            tzinfo = self.tzinfo
        if fold is None:
            fold = self.fold
        return type(self)(year, month, day, hour, minute, second,
                          microsecond, tzinfo, fold=fold)

    def _local_timezone(self):
        if self.tzinfo is None:
            ts = self._mktime()
        else:
            ts = (self - _EPOCH) // timedelta(seconds=1)
        localtm = _time.localtime(ts)
        local = datetime(*localtm[:6])
        # Extract TZ data
        gmtoff = localtm.tm_gmtoff
        zone = localtm.tm_zone
        return timezone(timedelta(seconds=gmtoff), zone)

    def astimezone(self, tz=None):
        if tz is None:
            tz = self._local_timezone()
        elif not isinstance(tz, tzinfo):
            raise TypeError("tz argument must be an instance of tzinfo")

        mytz = self.tzinfo
        if mytz is None:
            mytz = self._local_timezone()
            myoffset = mytz.utcoffset(self)
        else:
            myoffset = mytz.utcoffset(self)
            if myoffset is None:
                mytz = self.replace(tzinfo=None)._local_timezone()
                myoffset = mytz.utcoffset(self)

        if tz is mytz:
            return self

        # Convert self to UTC, and attach the new time zone object.
        utc = (self - myoffset).replace(tzinfo=tz)

        # Convert from UTC to tz's local time.
        return tz.fromutc(utc)

    # Ways to produce a string.

    def ctime(self):
        "Return ctime() style string."
        weekday = self.toordinal() % 7 or 7
        return "%s %s %2d %02d:%02d:%02d %04d" % (
            _DAYNAMES[weekday],
            _MONTHNAMES[self._month],
            self._day,
            self._hour, self._minute, self._second,
            self._year)

    def isoformat(self, sep='T', timespec='auto'):
        """Return the time formatted according to ISO.

        The full format looks like 'YYYY-MM-DD HH:MM:SS.mmmmmm'.
        By default, the fractional part is omitted if self.microsecond == 0.

        If self.tzinfo is not None, the UTC offset is also attached, giving
        giving a full format of 'YYYY-MM-DD HH:MM:SS.mmmmmm+HH:MM'.

        Optional argument sep specifies the separator between date and
        time, default 'T'.

        The optional argument timespec specifies the number of additional
        terms of the time to include. Valid options are 'auto', 'hours',
        'minutes', 'seconds', 'milliseconds' and 'microseconds'.
        """
        s = ("%04d-%02d-%02d%c" % (self._year, self._month, self._day, sep) +
             _format_time(self._hour, self._minute, self._second,
                          self._microsecond, timespec))

        off = self.utcoffset()
        tz = _format_offset(off)
        if tz:
            s += tz

        return s

    def __repr__(self):
        """Convert to formal string, for repr()."""
        L = [self._year, self._month, self._day,  # These are never zero
             self._hour, self._minute, self._second, self._microsecond]
        if L[-1] == 0:
            del L[-1]
        if L[-1] == 0:
            del L[-1]
        s = "%s.%s(%s)" % (self.__class__.__module__,
                           self.__class__.__qualname__,
                           ", ".join(map(str, L)))
        if self._tzinfo is not None:
            assert s[-1:] == ")"
            s = s[:-1] + ", tzinfo=%r" % self._tzinfo + ")"
        if self._fold:
            assert s[-1:] == ")"
            s = s[:-1] + ", fold=1)"
        return s

    def __str__(self):
        "Convert to string, for str()."
        return self.isoformat(sep=' ')

    @classmethod
    def strptime(cls, date_string, format):
        'string, format -> new datetime parsed from a string (like time.strptime()).'
        import _strptime
        return _strptime._strptime_datetime(cls, date_string, format)

    def utcoffset(self):
        """Return the timezone offset as timedelta positive east of UTC (negative west of
        UTC)."""
        if self._tzinfo is None:
            return None
        offset = self._tzinfo.utcoffset(self)
        _check_utc_offset("utcoffset", offset)
        return offset

    def tzname(self):
        """Return the timezone name.

        Note that the name is 100% informational -- there's no requirement that
        it mean anything in particular. For example, "GMT", "UTC", "-500",
        "-5:00", "EDT", "US/Eastern", "America/New York" are all valid replies.
        """
        if self._tzinfo is None:
            return None
        name = self._tzinfo.tzname(self)
        _check_tzname(name)
        return name

    def dst(self):
        """Return 0 if DST is not in effect, or the DST offset (as timedelta
        positive eastward) if DST is in effect.

        This is purely informational; the DST offset has already been added to
        the UTC offset returned by utcoffset() if applicable, so there's no
        need to consult dst() unless you're interested in displaying the DST
        info.
        """
        if self._tzinfo is None:
            return None
        offset = self._tzinfo.dst(self)
        _check_utc_offset("dst", offset)
        return offset

    # Comparisons of datetime objects with other.

    def __eq__(self, other):
        if isinstance(other, datetime):
            return self._cmp(other, allow_mixed=True) == 0
        elif not isinstance(other, date):
            return NotImplemented
        else:
            return False

    def __le__(self, other):
        if isinstance(other, datetime):
            return self._cmp(other) <= 0
        elif not isinstance(other, date):
            return NotImplemented
        else:
            _cmperror(self, other)

    def __lt__(self, other):
        if isinstance(other, datetime):
            return self._cmp(other) < 0
        elif not isinstance(other, date):
            return NotImplemented
        else:
            _cmperror(self, other)

    def __ge__(self, other):
        if isinstance(other, datetime):
            return self._cmp(other) >= 0
        elif not isinstance(other, date):
            return NotImplemented
        else:
            _cmperror(self, other)

    def __gt__(self, other):
        if isinstance(other, datetime):
            return self._cmp(other) > 0
        elif not isinstance(other, date):
            return NotImplemented
        else:
            _cmperror(self, other)

    def _cmp(self, other, allow_mixed=False):
        assert isinstance(other, datetime)
        mytz = self._tzinfo
        ottz = other._tzinfo
        myoff = otoff = None

        if mytz is ottz:
            base_compare = True
        else:
            myoff = self.utcoffset()
            otoff = other.utcoffset()
            # Assume that allow_mixed means that we are called from __eq__
            if allow_mixed:
                if myoff != self.replace(fold=not self.fold).utcoffset():
                    return 2
                if otoff != other.replace(fold=not other.fold).utcoffset():
                    return 2
            base_compare = myoff == otoff

        if base_compare:
            return _cmp((self._year, self._month, self._day,
                         self._hour, self._minute, self._second,
                         self._microsecond),
                        (other._year, other._month, other._day,
                         other._hour, other._minute, other._second,
                         other._microsecond))
        if myoff is None or otoff is None:
            if allow_mixed:
                return 2 # arbitrary non-zero value
            else:
                raise TypeError("cannot compare naive and aware datetimes")
        # XXX What follows could be done more efficiently...
        diff = self - other     # this will take offsets into account
        if diff.days < 0:
            return -1
        return diff and 1 or 0

    def __add__(self, other):
        "Add a datetime and a timedelta."
        if not isinstance(other, timedelta):
            return NotImplemented
        delta = timedelta(self.toordinal(),
                          hours=self._hour,
                          minutes=self._minute,
                          seconds=self._second,
                          microseconds=self._microsecond)
        delta += other
        hour, rem = divmod(delta.seconds, 3600)
        minute, second = divmod(rem, 60)
        if 0 < delta.days <= _MAXORDINAL:
            return type(self).combine(date.fromordinal(delta.days),
                                      time(hour, minute, second,
                                           delta.microseconds,
                                           tzinfo=self._tzinfo))
        raise OverflowError("result out of range")

    __radd__ = __add__

    def __sub__(self, other):
        "Subtract two datetimes, or a datetime and a timedelta."
        if not isinstance(other, datetime):
            if isinstance(other, timedelta):
                return self + -other
            return NotImplemented

        days1 = self.toordinal()
        days2 = other.toordinal()
        secs1 = self._second + self._minute * 60 + self._hour * 3600
        secs2 = other._second + other._minute * 60 + other._hour * 3600
        base = timedelta(days1 - days2,
                         secs1 - secs2,
                         self._microsecond - other._microsecond)
        if self._tzinfo is other._tzinfo:
            return base
        myoff = self.utcoffset()
        otoff = other.utcoffset()
        if myoff == otoff:
            return base
        if myoff is None or otoff is None:
            raise TypeError("cannot mix naive and timezone-aware time")
        return base + otoff - myoff

    def __hash__(self):
        if self._hashcode == -1:
            if self.fold:
                t = self.replace(fold=0)
            else:
                t = self
            tzoff = t.utcoffset()
            if tzoff is None:
                self._hashcode = hash(t._getstate()[0])
            else:
                days = _ymd2ord(self.year, self.month, self.day)
                seconds = self.hour * 3600 + self.minute * 60 + self.second
                self._hashcode = hash(timedelta(days, seconds, self.microsecond) - tzoff)
        return self._hashcode

    # Pickle support.

    def _getstate(self, protocol=3):
        yhi, ylo = divmod(self._year, 256)
        us2, us3 = divmod(self._microsecond, 256)
        us1, us2 = divmod(us2, 256)
        m = self._month
        if self._fold and protocol > 3:
            m += 128
        basestate = bytes([yhi, ylo, m, self._day,
                           self._hour, self._minute, self._second,
                           us1, us2, us3])
        if self._tzinfo is None:
            return (basestate,)
        else:
            return (basestate, self._tzinfo)

    def __setstate(self, string, tzinfo):
        if tzinfo is not None and not isinstance(tzinfo, _tzinfo_class):
            raise TypeError("bad tzinfo state arg")
        (yhi, ylo, m, self._day, self._hour,
         self._minute, self._second, us1, us2, us3) = string
        if m > 127:
            self._fold = 1
            self._month = m - 128
        else:
            self._fold = 0
            self._month = m
        self._year = yhi * 256 + ylo
        self._microsecond = (((us1 << 8) | us2) << 8) | us3
        self._tzinfo = tzinfo

    def __reduce_ex__(self, protocol):
        return (self.__class__, self._getstate(protocol))

    def __reduce__(self):
        return self.__reduce_ex__(2)
    """datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])

The year, month and day arguments are required. tzinfo may be None, or an
instance of a tzinfo subclass. The remaining arguments may be ints."""

