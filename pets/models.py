from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    rating = models.FloatField(default=0)
    total_ratings = models.PositiveIntegerField(default=0)
    is_subscribed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Animal(models.Model):
    BREED_CHOICES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('rabbit', 'Rabbit')
    ]

    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    adoption = models.BooleanField(default=False)
    breed = models.CharField(choices=BREED_CHOICES, max_length=20)
    description = models.TextField()
    age = models.PositiveIntegerField()
    sex = models.CharField(choices=SEX_CHOICES, max_length=1)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    picture = models.ImageField(upload_to='pet_adoption/images/', blank=True, null=True)
    purebred = models.BooleanField()
    neutered = models.BooleanField()

    def __str__(self):
        return f'{self.breed} - {self.age} years old'
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    wishlist = models.ManyToManyField(Animal, blank=True, related_name='whishlisted_by')

    def __str__(self):
        return f'{self.user.username} Profile'
    


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()



class Feedback(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Feedback by {self.buyer.username} to {self.seller.user.username}'


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} Wishlist'


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver}'
