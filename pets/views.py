from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView,DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, get_list_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Animal, Seller, Feedback, Wishlist,Message,Profile
from .forms import AnimalForm, FeedbackForm, AnimalSearchForm, SignUpForm,ProfileForm, WishlistForm
import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest

from .models import Wishlist



class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        # login(self.request, user)
        # return redirect('animal-list')
        return redirect('login')



class AnimalListView(ListView):
    model = Animal
    template_name = 'animal_list.html'
    context_object_name = 'animals'
    paginate_by = 3

    def get_queryset(self):
        queryset = Animal.objects.all()
        form = AnimalSearchForm(self.request.GET)

        if form.is_valid():
            name = form.cleaned_data.get('name')
            breed = form.cleaned_data.get('breed')
            animal_type = form.cleaned_data.get('animal_type')
            min_age = form.cleaned_data.get('min_age')
            max_age = form.cleaned_data.get('max_age')

            if name:
                queryset = queryset.filter(name__icontains=name)
            if breed:
                queryset = queryset.filter(breed__icontains=breed)
            if animal_type:
                queryset = queryset.filter(breed__icontains=animal_type)
            if min_age is not None:
                queryset = queryset.filter(age__gte=min_age)
            if max_age is not None:
                queryset = queryset.filter(age__lte=max_age)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AnimalSearchForm(self.request.GET)
        return context


class AnimalDetailView(DetailView):
    model = Animal
    template_name = 'animal_detail.html'
    context_object_name = 'animal'

    def get_object(self):
        return get_object_or_404(Animal, pk=self.kwargs['pk'])


class AnimalCreateView(CreateView):
    model = Animal
    form_class = AnimalForm
    template_name = 'animal_form.html'
    success_url = reverse_lazy('animal-list')

    def form_valid(self, form):
        form.instance.seller = self.request.user.seller
        return super().form_valid(form)


class AnimalUpdateView(UpdateView):
    model = Animal
    form_class = AnimalForm
    template_name = 'animal_form.html'
    success_url = reverse_lazy('animal-list')

class AnimalDeleteView(DeleteView):
    model = Animal
    template_name = 'animal_confirm_delete.html' 
    success_url = reverse_lazy('animal-list')

    def test_func(self):
        animal = self.get_object()
        return self.request.user == animal.owner or self.request.user.is_staff




class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    @property
    def user(self):
        return get_object_or_404(User, pk=self.request.user.id)

    def get_context_data(self):
        wishlist = Wishlist.objects.filter(user=self.request.user)
        # wishlist = get_list_or_404(Wishlist, user=self.user)
        return  {
            "wishlist": wishlist
        }
    


class FeedbackCreateView(LoginRequiredMixin, CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'feedback_form.html'

    def form_valid(self, form):
        form.instance.buyer = self.request.user
        form.instance.seller = get_object_or_404(Seller, id=self.kwargs['seller_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('animal_detail', kwargs={'pk': self.kwargs['animal_id']})


class WishlistAddView(View):
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('animal_detail', kwargs={'pk': self.kwargs['animal_id']})

    def post(self, request: HttpRequest, animal_id):
        user = get_object_or_404(User, pk=request.user.id)
        animal = get_object_or_404(Animal, pk=animal_id)
        model = Wishlist(user = user, animal = animal)
        model.save()
        return redirect("animal-list")

 

class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ['message']
    template_name = 'message_form.html'

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.receiver = get_object_or_404(User, id=self.kwargs['receiver_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('messages')


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'message_list.html'

    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user)




def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                profile = user.profile
            except Profile.DoesNotExist:
                profile = Profile.objects.create(user=user)
            login(request, user)
            return redirect('animal-list')
        else:
            return render(request, 'login.html', {'error': 'Wrong input data'})
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out!"))
    return redirect("animal-list")
