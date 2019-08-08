from rest_flex_fields import FlexFieldsModelSerializer
from .models import Application
from goods.serializers import GoodSerializer
from users.serializers import UserSerializer


class ApplicationSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Application
        exclude = ['date']

    expandable_fields = {
        'goods': (GoodSerializer, {'many': True}),
        'user': (UserSerializer, {})
    }
