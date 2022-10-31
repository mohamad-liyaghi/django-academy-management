from rest_framework import serializers
from rest_framework.exceptions import APIException
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


class CreateRequestSerializer(serializers.ModelSerializer):
    '''Create a new request'''

    id = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Request
        fields = ["id", "role", 'attachment', "description", "status", "date"]
    
    
    def validate_role(self, value):

        if self.context["user"].role in ["su", "ad"]:
            raise serializers.ValidationError("User is admin and rights were given.")

        if self.context['user'].role == "t" and value == "t":
            raise serializers.ValidationError("User is already a teacher.")
    
        if self.context["user"].requests.filter(status='p'):
            raise serializers.ValidationError("You already have a pending request.")

        return value


    def create(self, validated_data):
        validated_data.setdefault ("user", self.context["user"])
        return super().create(validated_data)