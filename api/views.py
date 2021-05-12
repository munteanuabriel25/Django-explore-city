from django.shortcuts import render, get_object_or_404
from rest_framework.parsers import JSONParser
from .serializer import ListingSerializer
from django.http import JsonResponse, HttpResponse
from listing.models import Listing
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@csrf_exempt
def ListingListAPI(request):
    
    if request.method=='GET':
        query = Listing.objects.all()
        serializer = ListingSerializer(query,many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method=='POST':
        data = JSONParser().parse(request)
        serializer = ListingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)

    
    
    
    
    
def ListingDetailAPI(request, pk):
    
    try:
        obj = get_object_or_404(Listing, pk=pk)
    except Listing.DoesNotExist:
        return HttpResponse(status=400)
        
    if request.method=='GET':
        serializer = ListingSerializer(obj)
        return JsonResponse(serializer.data, safe=False)
    
        