from rest_flex_fields import FlexFieldsModelSerializer
from .models import User

class UserSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = User
        exclude = []