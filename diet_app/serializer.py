from rest_framework import serializers
from diet_app.models import *


class Userserializer(serializers.ModelSerializer):
    profile=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=CustomUser
        fields=["id","username","email","password","phone","profile"]
        read_only_fields=["id"]
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data) 
    def get_profile(self,obj):
        profile_obj=UserProfile.objects.get(owner=obj)
        serializer_instance=Userprofileserializer(profile_obj)
        return serializer_instance.data




class Userprofileserializer(serializers.ModelSerializer):
    # view=serializers.SerializerMethodField()
    class Meta:
        model=UserProfile
        fields="__all__"
        read_only_fields=["id","bmr","owner"]

    # def get_profile(self,object):
    #     qs=UserProfile.objects.filter(user_object=object)
    #     d=Userserializer(qs,many=True)
    #     return d.data


class Foodlogserializer(serializers.ModelSerializer):
    class Meta:
        model=Foodlog
        fields="__all__" 
        read_only_fields=("id","owner","created_at")           