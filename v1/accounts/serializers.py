from rest_framework import serializers
from accounts.models import Profile


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