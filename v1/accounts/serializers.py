from rest_framework import serializers
from accounts.models import Profile


class ProfileListSerializer(serializers.ModelSerializer):
    '''List of all user profiles'''

    user = serializers.StringRelatedField()

    class Meta:
        model = Profile
        fields = ["id", "full_name", "passport_number", "user"]
