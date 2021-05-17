from listing.models import Listing, ListingCategory
from blog.models import Post
from user_profile.models import UserProfile
from rest_framework import serializers, viewsets
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token




class ListingCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingCategory
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = ['username','password','email']
        extra_kwargs = {'password': {'write_only': True},
                        'email': {'write_only': True}}
        
    def create(self, validated_data):
        user = User(email=validated_data['email'],
                    username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user
        
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, required=False)
    class Meta:
        model = UserProfile
        fields= '__all__'
        
class ListingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, required=False)
    class Meta:
        model = Listing
        fields ='__all__'

class PostSerializer(serializers.ModelSerializer):
    
    class Meta :
        model = Post
        fields = '__all__'
        
