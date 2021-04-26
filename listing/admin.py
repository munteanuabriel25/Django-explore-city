from django.contrib import admin
from .models import Listing, ListingCategory


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", ]
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(ListingCategory, CategoryAdmin)
admin.site.register(Listing)