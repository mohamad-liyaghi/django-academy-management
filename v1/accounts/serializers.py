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
            raise serializers.ValidationError("User already has a pending request.")
        
        if self.context["user"].requests.filter(status='b'):
            raise serializers.ValidationError("User is blocked.")

        return value


    def create(self, validated_data):
        validated_data.setdefault ("user", self.context["user"])
        return super().create(validated_data)


class RequestDetailSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField()

    class Meta:
        model = Request
        fields = ["id", "user", "role", "status", "attachment", "date", "description"]


class UpdateRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        fields = ["role", "status", "attachment", "description"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.context["user"].role in ["su", "ad"]:
            try:

                self.Meta.fields.remove("role")
                self.Meta.fields.remove('attachment')
                self.Meta.fields.remove('description')

            except: pass

        elif self.context["user"].role in ["s", "t"]:
            try:
                self.Meta.fields.remove("status")

            except: pass


    def update(self, instance, validated_data):
        '''Update user status if request was accepted'''
        
        if instance.status != "p":
            raise serializers.ValidationError("This case is closed.")

        request = super().update(instance, validated_data)        

        if request.status == "a":

            if request.role == "a":
                request.user.role = 'ad'
                request.user.save()

            elif request.role == "t":
                request.user.role = "t"
                request.user.save()

        return request         
