from rest_flex_fields import FlexFieldsModelSerializer
from users.serializers import UserSerializer
from .models import Good


class GoodSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Good
        exclude = []

    expandable_fields = {
        'user': (UserSerializer, {})
    }
