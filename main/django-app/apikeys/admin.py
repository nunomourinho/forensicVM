from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages
from .models import ChainOfCustody
from .models import ApiKey

class MaskedInput(forms.TextInput):
    """
    A custom form input widget that masks the input value.

    This widget replaces the actual value with a masked version for display purposes.
    The masked value consists of a configurable mask character repeated for the length
    of the value minus a specified mask length. The remaining characters at the end of
    the value are displayed as is.
    """
    def __init__(self, attrs=None, mask_char='*', mask_length=4):
        """
        Initialize the MaskedInput widget.

        Args:
            attrs (dict, optional): HTML attributes to be added to the rendered widget.
            mask_char (str, optional): The character used for masking the input value.
                Defaults to '*'.
            mask_length (int, optional): The number of characters to be masked at the
                beginning of the input value. Defaults to 4.
        """
        self.mask_char = mask_char
        self.mask_length = mask_length
        super().__init__(attrs)

    def format_value(self, value):
        """
        Formats the input value with masking.

        Args:
            value (str): The input value to be formatted.

        Returns:
            str: The masked value.
        """
        if value is None:
            return None
        masked_value = self.mask_char * (len(value) - self.mask_length)
        masked_value += value[-self.mask_length:]
        return masked_value

class ApiKeyForm(forms.ModelForm):
    """
    A form for the ApiKey model.

    This form specifies the model, fields, and any exclusions for the ApiKey model.
    It also defines a custom widget for the 'key' field to display a masked input.
    """
    class Meta:
        model = ApiKey
        fields = ['user']
        exclude = ['key']


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    """
    ModelAdmin for the ApiKey model.

    This ModelAdmin provides customizations for the admin interface for the ApiKey model.
    It specifies the form to use, the list display fields, and additional methods.
    """
    form = ApiKeyForm
    list_display = ('masked_key', 'created_at')

    def masked_key(self, obj):
        """
        Returns the masked version of the API key.

        This method takes an ApiKey object and returns a masked version of the API key.
        The masked version replaces most characters with a mask character, except for the
        last few characters which are displayed as is.
        """
        masked_key_length = 4
        if obj.key:
            key = str(obj.key)
            return f'{key[:masked_key_length]}{"*" * (len(key) - masked_key_length)}'
        else:
            return ""

    masked_key.short_description = 'Key'

    def get_queryset(self, request):
        """
        Returns the queryset of ApiKey objects.

        This method is used to filter the queryset of ApiKey objects based on the user's
        privileges. If the user is a superuser, all objects are returned. Otherwise, only
        the objects belonging to the user are returned.
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        """
        Saves the ApiKey object.

        This method is called when saving an ApiKey object through the admin interface.
        It sets the user attribute of the object to the current user and then saves the object.
        Additionally, it displays a success message with the generated API key.
        """
        obj.user = request.user
        super().save_model(request, obj, form, change)

        message = format_html('New API key generated: <strong><h2>{}</h2></strong>   Please copy it to the clipboard. This is the only time that this key is visible', obj.key)
        messages.success(request, message)



class ChainOfCustodyAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'action', 'parameters', 'ip_address','uuid')
    search_fields = ['user__username', 'action','ip_address','uuid']
    list_filter = ('date', 'user','ip_address','uuid')
    date_hierarchy = 'date'
    ordering = ['-date']

admin.site.register(ChainOfCustody, ChainOfCustodyAdmin)

