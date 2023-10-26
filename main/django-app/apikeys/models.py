from django.db import models
from django.contrib.auth.models import User
import uuid


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


class ChainOfCustody(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=500)
    parameters = models.TextField(blank=True, null=True)
    uuid = models.TextField(blank=False, null=False)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    ip_port = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} on {self.date.strftime('%Y-%m-%d %H:%M:%S')}"


class VMData(models.Model):
    REAL_IMAGE_CHOICES = [
        ('N/A', 'Not Applicable'),
        ('VMDK', 'VMDK'),
        ('ENCASE', 'Encase'),
        ('AFF', 'AFF'),
        ('RAW', 'RAW'),
        ('SMART', 'SMART'),
        ('QCOW2', 'QCOW2'),
    ]
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    uuid = models.CharField(max_length=36)
    conversion_time_txt = models.CharField(max_length=255, verbose_name="Conversion time: HH:MM:SS")
    extension = models.CharField(max_length=10, verbose_name="Disk image extension")
    filename = models.CharField(max_length=255, verbose_name="Disk image filename")
    image_type = models.CharField(max_length=50, verbose_name="Tool used to mount image")
    real_image_type = models.CharField(
        max_length=10,
        choices=REAL_IMAGE_CHOICES,
        default='N/A',
        verbose_name="Real image type"
    )
    mode = models.CharField(max_length=50, verbose_name="Conversion mode")
    conversion_time_in_seconds = models.FloatField(verbose_name="Real conversion time in seconds")
    disk_read = models.FloatField(verbose_name="Disk read test in MB/s")
    disk_write = models.FloatField(verbose_name="Disk write test in MB/s")
    elapsed_time = models.FloatField(verbose_name="Elapsed time in ticks")
    end_time = models.FloatField(verbose_name="End time in ticks")
    end_time_full = models.CharField(max_length=100, default='N/A', verbose_name="End time date")
    image_size = models.FloatField(verbose_name="Image size in bytes")
    start_time = models.FloatField(verbose_name="Start time in ticks")
    first_boot_time = models.FloatField(default=0, verbose_name="First boot time - Manual check")
    booted = models.BooleanField(default=False, verbose_name="If OS Booted - Manual check")
    start_time_full = models.CharField(max_length=100, default='N/A', verbose_name="Start time date")
    transfer_read_speed = models.FloatField(verbose_name="Network image read test in MB/s")
    distro = models.CharField(max_length=100, default='N/A', verbose_name="OS Distribution")
    hostname = models.CharField(max_length=100, default='N/A', verbose_name="Hostname")
    osinfo = models.CharField(max_length=100, default='N/A', verbose_name="OS Info")
    product_name = models.CharField(max_length=100, default='N/A', verbose_name="OS product name")
    image_source = models.CharField(max_length=100, default='N/A', verbose_name="Image site source")
    image_real_name = models.CharField(max_length=100, default='N/A', verbose_name="Image site identification")
    image_description = models.TextField(default='N/A', verbose_name="Image site description")
    class Meta:
        verbose_name = "Metric"

