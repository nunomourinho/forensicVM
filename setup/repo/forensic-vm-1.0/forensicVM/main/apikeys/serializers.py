"""
This code defines a serializer class ApiKeySerializer that is used to serialize and deserialize instances of the
ApiKey model.

The ApiKeySerializer class inherits from the ModelSerializer class provided by the Django REST Framework.
It specifies the ApiKey model as the model attribute in the Meta class.

The fields attribute in the Meta class specifies the fields that should be included in the serialized representation
of the ApiKey model. In this case, it includes only the key field.

By using this serializer, one can easily convert instances of the ApiKey model to JSON format (serialization) and
vice versa (deserialization) when working with API requests and responses.
"""
from rest_framework import serializers
from .models import ApiKey

class ApiKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiKey
        fields = ['key']

