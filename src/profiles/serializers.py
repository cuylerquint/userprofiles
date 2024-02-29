from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from rest_framework import serializers

from profile_app.utils import validate_email_address_format
from profiles.models import UserProfile


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=True)

    class Meta:
        fields = ("first_name", "last_name", "password", "email", "phone")

    def validate_phone(self, phone):
        is_already_exists = UserProfile.objects.filter(phone=phone).exists()
        if is_already_exists:
            raise ValidationError(f"The phone '{phone}' is already registered by another user!")
        return phone

    def validate_email(self, email):
        is_already_exists = UserProfile.objects.filter(user__email=email).exists()
        if is_already_exists:
            raise ValidationError(f"The email '{email}' is already registered by another user!",)

        if not validate_email_address_format(email):
            raise ValidationError(f"The email '{email}' is invalid format!")

        return email


class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="unique_id")
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    phone = serializers.CharField(read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "full_name",
        )

    def get_full_name(self, instance):
        return instance.user.get_full_name()


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        profile = UserProfile.objects.filter(user__email=data["email"]).first()
        if not profile:
            raise ValidationError("We can't seem to find a user with that information.")

        auth_user = authenticate(username=profile.user.username, **data)
        if auth_user:
            return profile
        raise AuthenticationFailed()



class UpdateEmailSerializer(serializers.Serializer):
    auth = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    token = serializers.CharField(max_length=255, required=True)

    def validate(self, data):
        user = (
            User.objects.filter(email=data["auth"]).first()
            or User.objects.filter(username=data["auth"]).first()
        )

        stripped_token = data["token"].replace(" ", "")

        token = UpdateEmailToken.objects.filter(
            created_user=user, token=stripped_token
        ).first()

        if not token:
            raise serializers.ValidationError("Invalid Token")

        data["auth"] = user
        data["token"] = token
        return data


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=False, allow_blank=False)
    email = serializers.CharField(required=False, allow_blank=False)
    first_name = serializers.CharField(required=False, allow_blank=False)
    last_name = serializers.CharField(required=False, allow_blank=False)

    class Meta:
        model = UserProfile
        fields = ("phone", "email", "first_name", "last_name")


    def validate_phone(self, phone):
        is_already_exists = UserProfile.objects.filter(phone=username).exists()
        if is_already_exists:
            raise ValidationError(
                detail=f"The phone '{phone}' is already registered by another user!",
                alert="error"
            )
        return username

    def validate_email(self, email):
        is_already_exists = UserProfile.objects.filter(email=email).exists()
        if is_already_exists:
            raise ValidationError(
                detail=f"The email '{email}' is already registered by another user!",
                alert="error",
            )

        if not validate_email_address_format(email):
            raise ValidationError(
                detail=f"The email '{email}' is invalid format!",
                alert="error",
            )

        return email