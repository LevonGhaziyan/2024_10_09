from django import forms
from .models import Animal, Feedback,Profile, Wishlist
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['breed', 'description', 'age', 'sex', 'price', 'picture', 'purebred', 'neutered']



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'city', 'country']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback']


class AnimalSearchForm(forms.Form):
    name = forms.CharField(required=False, label='Name')
    breed = forms.CharField(required=False, label='Breed')
    type_choices = [
        ('', ''),
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('rabbit', 'Rabbit')
    ]
    animal_type = forms.ChoiceField(choices=type_choices, required=False, label='Type')
    min_age = forms.IntegerField(required=False, label='Min Age')
    max_age = forms.IntegerField(required=False, label='Max Age')




class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    

class WishlistForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['wishlist']
        widgets = {
            'wishlist': forms.CheckboxSelectMultiple,
        }

