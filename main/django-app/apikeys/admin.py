from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages
from .models import ApiKey

class MaskedInput(forms.TextInput):
    def __init__(self, attrs=None, mask_char='*', mask_length=4):
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
    #key = forms.CharField(widget=MaskedInput(attrs={'readonly': 'readonly'}))
    #key = forms.CharField(disabled=False)
    class Meta:
        model = ApiKey
        fields = ['user']
        exclude = ['key']


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    form = ApiKeyForm
    list_display = ('masked_key', 'created_at')

    def masked_key(self, obj):
        masked_key_length = 4
        if obj.key:
            key = str(obj.key)
            return f'{key[:masked_key_length]}{"*" * (len(key) - masked_key_length)}'
        else:
            return ""

    masked_key.short_description = 'Key'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

        message = format_html('New API key generated: <strong><h2>{}</h2></strong>   Please copy it to the clipboard. This is the only time that this key is visible', obj.key)
        messages.success(request, message)


