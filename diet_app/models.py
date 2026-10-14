from django.db import models
from django.contrib.auth.models import AbstractUser
from diet_app.utility_function import calculate_bmr
# Create your models here.


class CustomUser(AbstractUser):
    phone=models.CharField(max_length=15,unique=True)


class UserProfile(models.Model):
    age=models.PositiveIntegerField()
    weight=models.FloatField()
    height=models.PositiveIntegerField()
    GENDER_OPTION=(('male','male'),('female','female'))

    gender=models.CharField(max_length=20,choices=GENDER_OPTION,default='male')


    ACTIVITY_OPTIONS=(
        ("1.2","Sedentary (little/no exercise)"),
        ("1.375","Lightly Active (exercise 1-3 days/weeks)"),
        ("1.55","Moderaltely Active (exercise 3-5 days/weeks)"),
        ("1.725","Very Active (exercise 6-7 days/weeks)"),
        ("1.9","Extra Active (Very intense Activity)"),
    ) 
    activity_level=models.CharField(max_length=120,choices=ACTIVITY_OPTIONS,default="1.2")
    bmr=models.FloatField(null=True)
    owner=models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name="profile")



    def save(self,*args,**kwargs):
        self.bmr=calculate_bmr(self.age,self.weight,self.height,self.gender,float(self.activity_level))
        return super().save(*args,**kwargs)


class Foodlog(models.Model):
    name=models.CharField(max_length=200,null=True)
    MEAL_TYPE_OPTIONS=(('breakfast','Breakfast'),
                       ('lunch','Lunch'),
                       ('dinner','Dinner'),
                       ('snack','Snack'))
    meal_type=models.CharField(max_length=100,choices=MEAL_TYPE_OPTIONS,null=True) 
    calories=models.PositiveIntegerField(null=True)
    serving_size=models.CharField(max_length=100,null=True)
    notes=models.TextField(null=True)
    picture=models.ImageField(upload_to='foodlog',null=True)
    owner=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="foodlog")
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name   