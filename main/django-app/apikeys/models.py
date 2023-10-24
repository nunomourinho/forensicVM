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

    def __str__(self):
        return f"{self.user.username} - {self.action} on {self.date.strftime('%Y-%m-%d %H:%M:%S')}"


class VMData(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    uuid = models.CharField(max_length=36)
    conversion_time_txt = models.CharField(max_length=255)
    extension = models.CharField(max_length=10)
    filename = models.CharField(max_length=255)
    image_type = models.CharField(max_length=50)
    real_image_type = models.CharField(max_length=50, default='N/A')
    mode = models.CharField(max_length=50)
    conversion_time_in_seconds = models.FloatField()
    disk_read = models.FloatField()
    disk_write = models.FloatField()
    elapsed_time = models.FloatField()
    end_time = models.FloatField()
    end_time_full = models.CharField(max_length=100, default='N/A')
    image_size = models.FloatField()
    start_time = models.FloatField()
    first_boot_time = models.FloatField(default=0)
    booted = models.BooleanField(default=False)
    start_time_full = models.CharField(max_length=100, default='N/A')
    transfer_read_speed = models.FloatField()
    distro = models.CharField(max_length=100, default='N/A')
    hostname = models.CharField(max_length=100, default='N/A')
    osinfo = models.CharField(max_length=100, default='N/A')
    product_name = models.CharField(max_length=100, default='N/A')
    image_source = models.CharField(max_length=100, default='N/A')
    image_real_name = models.CharField(max_length=100, default='N/A')
    image_description = models.TextField(default='N/A')


