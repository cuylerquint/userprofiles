import datetime
import logging
import traceback

from django.contrib.auth import login, logout
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from profiles.authentication import get_user_access_token
from profiles.models import AuthToken, UpdateEmailToken, User
from profiles.serializers import (LoginSerializer, RegisterSerializer,
                                  UpdateEmailSerializer, UserProfileSerializer)
from profiles.services import create_user_profile

logger = logging.getLogger(__name__)


class AuthViews(viewsets.ModelViewSet):
    allowed_methods = ("POST", "PATCH", "OPTIONS")
    action_permissions = {
        IsAuthenticated: ["update_email_request"],
        AllowAny: [
            "login",
            "register",
        ],
    }

    @action(methods=["POST"], detail=False, url_name="login", url_path="login")
    def login(self, request, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = serializer.validated_data

        jwt_token = get_user_access_token()
        AuthToken.objects.create(key=jwt_token, profile=profile)

        return Response(
            {
                "message": "Login Successful",
                "user": UserProfileSerializer(profile).data,
                "access_token": jwt_token,
            },
            status=200,
        )

    @action(
        methods=["POST"],
        detail=False,
        url_name="register",
        url_path="register",
    )
    def register(self, request, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        profile = create_user_profile(serializer.data)

        jwt_token = get_user_access_token()
        AuthToken.objects.create(key=jwt_token, profile=profile)

        return Response(
            {
                "user": UserProfileSerializer(profile).data,
                "access_token": jwt_token,
            },
            status=200,
        )

    @action(
        methods=["POST"],
        detail=False,
        url_name="update-email-request",
        url_path="update-email-request",
    )
    def update_email_request(self, request, **kwargs):
        serializer = UpdateEmailRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("auth")
        ten_mins_ago = datetime.datetime.now() - datetime.timedelta(minutes=10)
        existing_token = UpdateEmailToken.objects.filter(
            created_user=user,
            email=serializer.validated_data.get("email"),
            created_dttm__gt=ten_mins_ago,
        ).first()
        if existing_token:
            email_token = existing_token
        else:
            email_token = UpdateEmailToken.objects.create(
                created_user=user, token=random_digit_str(6)
            )

        if email_token:
            # TODO Email Service
            # EmailService(
            #     to_user=user,
            #     template=EmailTemplates.UPDATE_EMAIL,
            #     kwargs={
            #         "token": email_token.__str__(),
            #         "to_email": serializer.validated_data["email"],
            #     },
            # )
            return Response(
                {
                    "message": "An email has been sent to the new email for confirmation."
                },
                status=200,
            )
        else:
            return Response(
                {
                    "message": "creating update email token failed"
                },
                status=400,
            )
