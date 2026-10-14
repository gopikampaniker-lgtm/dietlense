from django.shortcuts import render
from diet_app.models import *
from diet_app.serializer import *
from rest_framework.generics import CreateAPIView,RetrieveAPIView,UpdateAPIView,ListAPIView,DestroyAPIView
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from diet_app.utility_function import calculate_bmr
from diet_app.permission import Isowner
from django.db.models import Sum
from rest_framework.response import Response
from django.utils import timezone
# Create your views here.
class Signup(CreateAPIView):
    serializer_class=Userserializer


class Profileview(CreateAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    serializer_class=Userprofileserializer


    def perform_create(self, serializer):
        user_obj=self.request.user
        # data=serializer.validated_data
        # bmr=calculate_bmr(
        #     age=data.get('age'),
        #     height=data.get('height'),
        #     weight=data.get('weight'),
        #     gender=data.get('gender'),
        #     activity_level=data.get('activity_level')
        # )
        return serializer.save(owner=user_obj)


class Profileretrive(RetrieveAPIView,UpdateAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[Isowner]
    serializer_class=Userprofileserializer
    queryset=UserProfile.objects.all()


class UserRetriveview(RetrieveAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[Isowner]
    serializer_class=Userserializer
    queryset=CustomUser.objects.all()



class Foodlogcreatedlistview(CreateAPIView,ListAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    serializer_class=Foodlogserializer
    queryset=Foodlog.objects.all()


    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)



class FoodlogRetriveUpdateDestroy(RetrieveAPIView,UpdateAPIView,DestroyAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[Isowner]
    serializer_class=Foodlogserializer
    queryset=Foodlog.objects.all()    



class Dietsummery(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[Isowner]
    def get(self,request,*args,**kwargs):
        cur_date=timezone.now()
        queryset=Foodlog.objects.filter(created_at__date=cur_date,owner=request.user)
        ser=Foodlogserializer(queryset,many=True)
        calories_consumed=queryset.values("calories").aggregate(Sum('calories'))
        print(calories_consumed)
        print(request.user.profile.bmr)
        context={
            "total_calories_consumed":calories_consumed.get('calories__sum'),
             "daily_target":request.user.profile.bmr,"balance":request.user.profile.bmr-calories_consumed.get('calories__sum')
        }
        return Response(context)
        

