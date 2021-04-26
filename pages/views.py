from django.shortcuts import render
from django.http import HttpResponse
from listing.models import ListingCategory
# Create your views here.

def home_view(request):
    categories= ListingCategory.objects.all()
    return render(request, 'pages/home.html',{'categories':categories})