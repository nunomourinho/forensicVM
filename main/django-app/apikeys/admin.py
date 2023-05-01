from django import forms
from django.contrib import admin
from .models import ApiKey

class MaskedInput(forms.TextInput):
    def __init__(self, attrs=None, mask_char='*', mask_length=8):
        self.mask_char = mask_char
        self.mask_length = mask_length
        super().__init__(attrs)

    def format_value(self, value):
        if value is None:
            return None
        masked_value = self.mask_char * (len(value) - self.mask_length)
        masked_value += value[-self.mask_length:]
        return masked_value

class ApiKeyForm(forms.ModelForm):
    key = forms.CharField(widget=MaskedInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = ApiKey
        fields = ['user', 'key']

@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    form = ApiKeyForm
    list_display = ('masked_key', 'created_at')

    def masked_key(self, obj):
        masked_key_length = 8
        masked_key = '*' * (len(obj.key) - masked_key_length)
        masked_key += obj.key[-masked_key_length:]
        return masked_key
    masked_key.short_description = 'Key'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

