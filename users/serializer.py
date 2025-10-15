from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','password')
        read_only_fields = ('id',)

    def create(self, validated_data)-> User:
        password = validated_data.pop('password')
        new_user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('firts_name',''),
            last_name=validated_data.get('last_name','')
        )

        return new_user
    
    def update(self, instance, validated_data)-> User:
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)     
        return instance