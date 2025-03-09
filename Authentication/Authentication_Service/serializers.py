from rest_framework import serializers
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='name', required=False)   
    
    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'password', 'username')
        extra_kwargs = {
            'password': {'write_only': True},
            'name': {'required': False}    
        }
    
    def validate(self, data):
 
        if 'name' not in data and 'username' in data:
            data['name'] = data['username']
  
        if 'name' not in data:
            raise serializers.ValidationError("Either 'name' or 'username' must be provided")
        return data

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
