from django.shortcuts import render, get_object_or_404
from .serializer import ListingSerializer, \
    ListingCategorySerializer, \
    PostSerializer, \
    UserProfileSerializer, \
    CommentSerializer, \
    UserSerializer,ListingWishListSerializer
    
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
    """this view manages GET,POST requests for Listing Category [list] and also for all Listings [list] atashed to a speciffic category"""
    def get(self, request,categ_name=None):
        if categ_name != None:
            query = Listing.objects.filter(category__slug=categ_name)
            serializer = ListingSerializer(query, many=True)
            return  Response(serializer.data, status=status.HTTP_200_OK)
        else:
            query = ListingCategory.objects.all()
            serializer = ListingCategorySerializer(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request, categ_name=None):
        
            serializer = ListingSerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    
    
class ListingDetailApiView(APIView):
    """ this view manages GET,PUT,DELETE  requests for a specific ID from a specific category SLUG"""
    def get_data(self,categ_name, pk):
        data = get_object_or_404(Listing,category__slug=categ_name,pk=pk)
        return data
    
    def get(self, request,categ_name, pk):
        serializer = ListingSerializer(self.get_data(categ_name, pk))
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self,request,categ_name,pk):
        instance = self.get_data(categ_name,pk)
        instance.delete()
        return Response({"Success": "Listig deleted succesfully"}, status=status.HTTP_202_ACCEPTED)

    def put(self, request, categ_name,pk):
        instace = self.get_data(categ_name, pk)
        serializer = ListingSerializer(instace, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data,status=status.HTTP_200_OK )
        else:
            return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST )
    
    

class PostListingApiView(APIView):
    
    def get_data(self, pk):
        instance = get_object_or_404(Post, pk=pk)
        return instance
    
    def get(self,request, pk=None):
        if pk == None:
            query = Post.objects.all()
            serializer = PostSerializer(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            instance = self.get_data(pk)
            serializer= PostSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def post(self,request):
        user = get_user_model().objects.get(username=request.user)
        serializer=  PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user = user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    def delete(self,request,pk):
        user = get_user_model().objects.get(username=request.user)
        instance = self.get_data(pk)
        if instance.user == user:
            instance.delete()
            return Response({"Success: Post Instance Deleted Successfully" })
        else:
            return Response({"Errror: Don't have rights to perform this operation" }, status=status.HTTP_403_FORBIDDEN)
        
    def put(self,request,pk):
        user = get_user_model().objects.get(username=request.user)
        instance = self.get_data(pk)
        if instance.user == user:
            serializer = PostSerializer(instance=instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST )
        else:
            return Response({"Errror: Don't have rights to perform this operation"}, status=status.HTTP_403_FORBIDDEN)
        
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
       
    
            
class ListingWishListAPIView(APIView):
    def post(self, request):
        serializer = ListingWishListSerializer(data=request.data)
        if serializer.is_valid():
            user = get_user_model().objects.get(pk=serializer.validated_data["user_id"])
            listing = Listing.objects.get(pk=serializer.validated_data["listing_id"])
            # check if user wants to add or to remove this item from wishlist
            # then perform the appropiate action and return JSON response with status
            if listing.wishlist.filter(id=user.id).exists():
                listing.wishlist.remove(user)
                listing.save()
            
                return Response(data={'text': "add wishlist"}, status=status.HTTP_200_OK)
            else:
                listing.wishlist.add(user)
                listing.save()
               
                return Response(data={'text': "del wishlist"}, status=status.HTTP_200_OK)
    