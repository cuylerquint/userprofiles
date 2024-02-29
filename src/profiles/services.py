import uuid

from django.db import transaction

from profiles.models import User, UserProfile


@transaction.atomic
def create_user_profile(validated_data):
    """Persist User and UserProfile into database from validated serializer."""
    user_data = {
        "username": validated_data['email'],
        "first_name": validated_data['first_name'],
        "last_name": validated_data['last_name'],
        "email": validated_data['email'],
        "is_active": True,
    }

    user = User.objects.create_user(**user_data)

    user.set_password(raw_password=validated_data['password'])
    user.save()

    user_profile_data = {
        "user": user,
        "unique_id": uuid.uuid4(),
        "phone": validated_data['phone']
    }
    profile, created = UserProfile.objects.get_or_create(
        **user_profile_data
    )

    return profile