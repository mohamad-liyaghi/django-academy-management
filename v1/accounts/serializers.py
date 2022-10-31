from rest_framework import serializers
from accounts.models import Profile, Request


class ProfileListSerializer(serializers.ModelSerializer):
    '''List of all user profiles'''

    user = serializers.StringRelatedField()

    class Meta:
        model = Profile
        fields = ["id", "full_name", "passport_number", "user"]


class ProfileDetailSerializer(serializers.ModelSerializer):
    '''Profile detail/update serializer'''

    class Meta:
        model = Profile
        fields = ["id", "full_name", "first_name", "last_name", "picture", 
                    "age", "phone_number", "address", "passport_number"]


class RequestListSerializer(serializers.ModelSerializer):
    '''List of all user requests'''

    user = serializers.StringRelatedField()
    class Meta:
        model = Request
        fields = ["id", "user", "role", "status"]