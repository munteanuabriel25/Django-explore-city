from django.shortcuts import render, get_object_or_404
from .serializer import ListingSerializer, \
    ListingCategorySerializer, \
    PostSerializer, \
    UserProfileSerializer, \
    CommentSerializer, \
    UserSerializer
    
from listing.models import Listing, ListingCategory
from blog.models import Post, Comment
from user_profile.models import UserProfile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

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
        
        
class CommentActionApiView(APIView):
    """This API view is used by django template  who send an ajax POST request for specific action: add commment,delete comment, update comment"""
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        comment_id = request.data['id']
        if request.data.get("action")=="delete":
            comment_obj = get_object_or_404(Comment, pk=comment_id)
            comment_obj.delete()
            return Response({'status':'deleted'}, status=status.HTTP_200_OK)
    
    def put(self, request):
        comment_id = request.data['id']
        comment_obj = get_object_or_404(Comment, pk=comment_id)
        if request.data.get("action")=="put":
            # this call returns an editable html comment
            serializer = CommentSerializer(comment_obj, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    def patch(self, request):
        comment_id = request.data['id']
        comment_obj = Comment.objects.get(id=comment_id)
        serializer = CommentSerializer(comment_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': True}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors)
       
    
            
            