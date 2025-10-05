from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class UserRegistrationSerializer(serializers.ModelSerializer):
    # Accept either the internal choice key (e.g. 'student') or the human label
    # (e.g. 'Student'), case-insensitively.
    role = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def validate_role(self, value):
        # Normalize and accept either key or label (case-insensitive)
        # ROLE_CHOICES is a tuple of (key, label)
        keys = [k for k, _ in User.ROLE_CHOICES]
        label_to_key = {label.lower(): key for key, label in User.ROLE_CHOICES}

        if value in keys:
            return value

        low = value.lower()
        if low in keys:
            return low

        if low in label_to_key:
            return label_to_key[low]

        # Also allow Title-cased labels that might not match lower() exactly
        for key, label in User.ROLE_CHOICES:
            if value == label:
                return key

        raise serializers.ValidationError(f'"{value}" is not a valid choice.')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
