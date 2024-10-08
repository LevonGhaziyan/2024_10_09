from . import views
from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from .views import AnimalUpdateView,AnimalListView, AnimalDetailView, AnimalCreateView, FeedbackCreateView, WishlistAddView, SignUpView
from .views import MessageCreateView, MessageListView,ProfileUpdateView,AnimalDeleteView

urlpatterns = [
    path('', AnimalListView.as_view(), name='animal-list'), 
    path('animal/<int:pk>/', AnimalDetailView.as_view(), name='animal_detail'),
    path('animal/add/', AnimalCreateView.as_view(), name='animal-add'),
    path('animal/edit/<int:pk>/', AnimalUpdateView.as_view(), name='animal-edit'),
    path('animal/<int:pk>/delete/', AnimalDeleteView.as_view(), name='animal_delete'),
    path('search/', AnimalListView.as_view(), name='animal-search'),
    path('feedback/<int:seller_id>/<int:animal_id>/', FeedbackCreateView.as_view(), name='feedback-create'),
    path('wishlist/add/<int:animal_id>/', WishlistAddView.as_view(), name='wishlist-add'),

    path('message/send/<int:receiver_id>/', MessageCreateView.as_view(), name='send-message'),
    path('messages/', MessageListView.as_view(), name='messages'),
    path('animal-cruelty/', TemplateView.as_view(template_name='animal_cruelty.html'), name='animal-cruelty'),

    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('signup/', SignUpView.as_view(), name='signup'),

    path('profile/', ProfileUpdateView.as_view(), name='profile'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



