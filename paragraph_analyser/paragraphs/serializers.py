# serializers.py
from rest_framework import serializers
from .models import Paragraph, CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # To hide password in response

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "password",
            "email",
            "dob",
            "createdAt",
            "modifiedAt",
        ]
        read_only_fields = [
            "id",
            "createdAt",
            "modifiedAt",
        ]  # Fields that should not be modified directly

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data["username"],
            email=validated_data["email"],
            dob=validated_data.get("dob", None),  # Optional field
        )
        user.set_password(validated_data["password"])  # Set hashed password
        user.save()
        return user


class ParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paragraph
        fields = ["id", "content"]
