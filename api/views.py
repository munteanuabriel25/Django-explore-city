from django.shortcuts import render, get_object_or_404
from .serializer import ListingSerializer, ListingCategorySerializer, PostSerializer, UserProfileSerializer
from listing.models import Listing, ListingCategory
from blog.models import Post
from user_profile.models import UserProfile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.contrib.auth import authenticate
# Create your views here.


class ListingCategApiView(APIView):
    """this view manages GET requests for Listing Category [list] and also for all Listings [list] atashed to a speciffic category"""
    def get(self, request,categ_name=None):
        if categ_name != None:
            query = Listing.objects.filter(category__slug=categ_name)
            serializer = ListingSerializer(query, many=True)
            return  Response(serializer.data, status=status.HTTP_200_OK)
        else:
            query = ListingCategory.objects.all()
            serializer = ListingCategorySerializer(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
class ListingDetailApiView(APIView):
    
    def get(self, request,categ_name, pk):
        data = get_object_or_404(Listing,
                                 category__slug=categ_name,
                                 pk=pk)
        serializer = ListingSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class PostListingApiView(APIView):
    def get(self,request):
        query = Post.objects.all()
        serializer = PostSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
        
class UserCreateApiView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    def get(self, request):
            return JsonResponse({'DATA':"FDFD"})
    
class UserLoginApiView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request,username=username, password=password)
        
        if user is not None:
            user_profile = UserProfile.objects.get(user=user)
            user_serializer = UserProfileSerializer(user_profile)
            return Response({'token': user.auth_token.key, 'user_profile':user_serializer.data })
        else:
            return Response({'error': 'Wrong credentials'}, status=status.HTTP_400_BAD_REQUEST)