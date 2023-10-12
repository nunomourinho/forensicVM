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

    def __str__(self):
        return f"{self.user.username} - {self.action} on {self.date.strftime('%Y-%m-%d %H:%M:%S')}"

