from django.urls import path
from . import views
from .views import * 
from django.contrib.auth.views import LogoutView

urlpatterns=[
    path('login/', views.loginPage, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.index, name='vips'),
    path('user-vip/', views.uservips, name='user-vip'),
    path('profile/', views.profile, name='user-profile'),
    path('contact/', Contact.as_view(), name='contact' ),
    path('contact/success/',views.contact_success, name='contact_success' ),
    path('user-speaker/', views.userSpeaker, name='user-speaker'),
    path('add-speaker/<slug:vip_slug>', views.addSpeaker, name='add-speaker'),
    path('speaker-details/<int:id>', views.speakerDetails, name='speaker-details'),
    path('speaker-update/<int:id>', SpeakerUpdate.as_view(), name='speaker-update'),
    path('speaker-delete/<int:id>', SpeakerDelete.as_view(), name='speaker-delete'),
    
    
    path('vip-details/<slug:vip_slug>', views.vip_details, name='vip-details'),
    path('vip-create', vipsCreate.as_view() , name='vip-create'),
    path('vip-update/<slug:slug>', vipUpdate.as_view() , name='vip-update'),
    path('vip-delete/<slug:slug>', vipDelete.as_view() , name='vip-delete'),
    path('participants/<int:id>', views.participant, name='participants'),
    path('confirm/',views.confirmParticipation, name='confirm-registration'),
   


]