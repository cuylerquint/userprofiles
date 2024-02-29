import datetime

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from profiles.models import UpdateEmailToken, UserProfile
from profiles.serializers import UserProfileSerializer


class ProfileViews(viewsets.ModelViewSet):
    allowed_methods = ("GET",)
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.all()


    # TODO add authentication to update a users data
    def partial_update(self, request, *args, **kwargs):
        if self.requesting_account.user != request.user:
            raise PermissonError("Cannot update another user's profile")

        serializer = UserProfileUpdateSerializer(
            self.requesting_account, data=request.data, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        update_email = False
        if (
                serializer.validated_data.get("email")
                and serializer.validated_data["email"]
                != self.request.user.email
        ):
            # start email reset flow
            update_email = True
            new_email = serializer.validated_data.get("email")
            del serializer.validated_data["email"]

        serializer.save()

        if update_email:

            ten_mins_ago = datetime.datetime.now() - datetime.timedelta(minutes=10)

            existing_token = UpdateEmailToken.objects.filter(
                created_user=self.requesting_account.user,
                email=new_email,
                created_dttm__gt=ten_mins_ago,
            ).first()

            if existing_token:
                email_token = existing_token
            else:
                email_token = UpdateEmailToken.objects.create(
                    created_user=self.requesting_account.user,
                    token=random_digit_str(6),
                )

            # TODO Email Service
            # EmailService(
            #     to_user=self.requesting_account.user,
            #     template=EmailTemplates.UPDATE_EMAIL,
            #     kwargs={"token": email_token.__str__(), "to_email": new_email},
            # )



            request_handler.success(
                detail="Profile updated successfully. "
                       "An email has been sent to the new email location for confirmation.",
                append_emoji=True,
            )
        else:
            request_handler.success(
                detail="Profile updated successfully!", append_emoji=True
            )
