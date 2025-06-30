from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['owner', 'created_at', 'updated_at']
    
    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title must not be empty.")
        return value
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        # read_only_fields = ['username']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class LoginSerializers(serializers.Serializer):
    username = serializers.CharField(max_length = 150, required=True)
    password = serializers.CharField(max_length=128, write_only=True, required=True)
    