from listing.models import Listing
from rest_framework import serializers, viewsets


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields ='__all__'
        
        
