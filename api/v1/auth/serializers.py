from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from api.v1.user.serializers import UserSerializerWithToken

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user)
        data.update(serializer.data)
        return data