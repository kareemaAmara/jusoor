from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Organization


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    org_name = serializers.CharField(required=False, allow_blank=True, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'phone', 'role', 'skills', 'org_name']

    def create(self, validated_data):
        org_name = validated_data.pop('org_name', None)
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # If organization, create Organization record
        if user.role == 'organization' and org_name:
            Organization.objects.create(user=user, org_name=org_name)

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            # Try by email
            try:
                u = User.objects.get(email=data['email'])
                user = authenticate(username=u.username, password=data['password'])
            except User.DoesNotExist:
                pass

        if not user:
            raise serializers.ValidationError("Invalid email or password")
        if not user.is_active:
            raise serializers.ValidationError("Account is disabled")

        data['user'] = user
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'role', 'skills', 'profile_image', 'created_at']
        read_only_fields = ['id', 'role', 'created_at']


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'org_name', 'description', 'website', 'address', 'verified']
        read_only_fields = ['id', 'verified']