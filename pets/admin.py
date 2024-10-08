from django.contrib import admin

from .models import Seller, Animal, Feedback, Wishlist

from django.contrib.auth.models import User
from .models import Profile


class SellerAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_subscribed')  
    list_filter = ('is_subscribed',)  
    list_editable = ('is_subscribed',)

admin.site.register(Seller,SellerAdmin)
admin.site.register(Animal)
admin.site.register(Feedback)
admin.site.register(Wishlist)
admin.site.register(Profile)


for user in User.objects.all():
    Profile.objects.get_or_create(user=user)



