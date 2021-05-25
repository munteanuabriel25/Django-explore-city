from listing.models import Listing, ListingCategory
from blog.models import Post, Comment
from user_profile.models import UserProfile
from rest_framework import serializers, viewsets, fields
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from datetime import datetime


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields= '__all__'


class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'email', "userprofile"]
        extra_kwargs = {'password': {'write_only': True},
                        'email': {'write_only': True}}


class ListingCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingCategory
        fields = '__all__'
    
    def create(self, validated_data):
        user = User(email=validated_data['email'],
                    username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user



class ListingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Listing
        fields ='__all__'



class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, required=False)
    class Meta :
        model = Post
        fields = '__all__'



class CommentSerializer(serializers.ModelSerializer):
    user_pic = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    pub_date = serializers.SerializerMethodField()
    
    class Meta :
        model = Comment
        fields = "__all__"
        
    def get_pub_date(self, obj):
        t=obj.pub_date
        x = t.strftime("%d %b %Y - %H:%M %p ")
        return x
    
    def get_user_pic(self, obj):
        return obj.user.userprofile.picture.url
    
    def get_user_name(self, obj):
        return obj.user.userprofile.username
    
    

class ListingWishListSerializer(serializers.Serializer):

    user_id= serializers.IntegerField(required=True)
    listing_id = serializers.IntegerField(required=True)
    


    

    