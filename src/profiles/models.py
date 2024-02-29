import uuid

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    created_dttm = models.DateTimeField(auto_now_add=True)
    updated_dttm = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True
    )  # username, first, last, email
    phone = models.CharField(max_length=100, null=True, blank=False)
    unique_id = models.UUIDField(unique=True)

    class Meta:
        ordering = ["-created_dttm"]

    def __str__(self):
        return "{}".format(self.user.username)



class UpdateEmailToken(models.Model):
    key = models.CharField(max_length=6, primary_key=True, blank=False, editable=False)
    profile = models.ForeignKey(
        UserProfile, related_name="update_email_token", on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    email = models.CharField(max_length=256, null=False, blank=False)

    def __str__(self):
        return " ".join([char for char in list(self.key)])

    class Meta:
        verbose_name = "update-email-token"
        verbose_name_plural = "update-email-token"
        db_table = "update_email_token"



class AuthToken(models.Model):
    key = models.CharField(max_length=256, primary_key=True, editable=False)
    profile = models.ForeignKey(UserProfile, related_name="auth_token", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "active-auth-token"
        verbose_name_plural = "active-auth-tokens"
        db_table = "active_auth_token"
