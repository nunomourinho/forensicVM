from django.db import models
from django.contrib.auth.models import User

class ApiKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def mask_key(self):
        masked_key_length = 8
        masked_key = '*' * (len(self.key) - masked_key_length)
        masked_key += self.key[-masked_key_length:]
        return masked_key

    def __str__(self):
        return self.mask_key()

