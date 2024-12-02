from django.shortcuts import render, redirect
from django.http import HttpResponse
from.models import vip, myUser
from django.views.generic import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from.forms import *
from django.views.generic import FormView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from string import punctuation
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.
#login user
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('vips')
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        email.lower()
        try:
            user=myUser.objects.get(email=email)
        except:
            messages.error(request, ' email does not exist')
        user=authenticate(request, email=email, password=password)
        if user is not None:
            login(request,user)
            return redirect('vips')
        else:
            messages.error(request, 'invalid credential')
    return render(request, 'vip/login.html')







def register(request):
    form=MyUserRegistrationForm()
    if request.method=='POST':
        form=MyUserRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request, user)
            return redirect('vips')
        else:
             messages.error(request, 'An error occurred during registration')

    return render(request, 'vip/register.html', {'form':form})


def index(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    vips=vip.objects.filter(activate=True)
    vips=vips.filter(
        Q(title__icontains=q)|
          Q(description__icontains=q)|
          Q(location_name__icontains=q)
       
        )
    
    count=vips.count()
   # user=myUser.objects.get(id=request.user.id)
    return render(request, 'vip/index.html' , {'vips':vips, 'count':count})


def vip_details(request, vip_slug):
 selected_vip=vip.objects.get(slug=vip_slug)
 speakers=selected_vip.vip_speakers.all
 if request.method=='GET':
     form=ParticipantForm()
 else:
      form=ParticipantForm(request.POST)
      if form.is_valid():
          participant=form.save()
          selected_vip.participant.add(participant)
          return redirect('confirm-registration')
 return render (request, 'vip/vip_detail.html', {'vip':selected_vip, 'speakers':speakers, 'form':form})

@login_required(login_url='login')
def uservips(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    user_vips=vip.objects.order_by('-create')
    user_vips=vip.objects.filter(activate=True)
    user_vips=user_vips.filter(user=request.user)

    user_vips=user_vips.filter(
        Q(title__icontains=q)|
          Q(description__icontains=q)|
          Q(location_name__icontains=q)
       
        )
    
    count=user_vips.count()
    return render(request, 'vip/user_vip.html', {'user_vips':user_vips, 'count':count})


@login_required(login_url='login')
def addSpeaker(request, vip_slug):
    selected_vip=vip.objects.get(slug=vip_slug)
    if request.method=='GET':
           form=SpeakerRegistration()
    else:
    
        form=SpeakerRegistration(request.POST, request.FILES)
        if form.is_valid():
                form.instance.user=request.user
                speaker=form.save(commit=False)
                form.instance.vip_name=selected_vip.title
                speaker=form.save()
                selected_vip.vip_speakers.add(speaker)
                return redirect('vips')
              
    return render(request,'vip/add_speaker.html',{'vip':selected_vip, 'form':form })

@login_required(login_url='login')
def userSpeaker(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    user_speakers=Speaker.objects.order_by('-id')
    user_speakers=user_speakers.filter(user=request.user)
    user_speakers= user_speakers.filter(
        Q(name__icontains=q)|
          Q(vip_name__icontains=q)  
        )
    
    count=user_speakers.count()
    return render(request, 'vip/user_speaker.html', {'user_speakers':user_speakers,'count':count})


@login_required(login_url='login')
def speakerDetails(request, id):
    speaker=Speaker.objects.get(pk=id)
    return render(request, 'vip/speaker_details.html', {'speaker':speaker})


class vipUpdate(LoginRequiredMixin,UpdateView):
   model=vip
   form_class=UservipForm
   template_name='vip/vip_form.html'
   success_url=reverse_lazy('vips')
   slug_field='slug'
   def form_valid(self, form):
        form.instance.user=self.request.user
        return super(vipUpdate, self).form_valid(form)


#speakers update
class SpeakerUpdate(LoginRequiredMixin,UpdateView):
    model=Speaker
    form_class = SpeakerRegistration
    pk_url_kwarg='pk'
    template_name='vip/add_speaker.html'
    success_url=reverse_lazy('vips')
    
    
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(SpeakerUpdate, self).form_valid(form)
    
#Delete Speakers
class SpeakerDelete(LoginRequiredMixin,DeleteView):
    model=Speaker
    context_object_name='speaker'
    template_name='vip/delete_speaker.html'
    success_url=reverse_lazy('user-speaker')

#Delete vips
class vipDelete(LoginRequiredMixin,DeleteView):
    model=vip
    context_object_name='vip'
    slug_field='slug'
    template_name='vip/delete_vip.html'
    success_url=reverse_lazy('user-vip')  

#add vips class
class vipsCreate(LoginRequiredMixin,CreateView):
    model=vip
    form_class = UservipForm
   
    success_url=reverse_lazy('vips')
    template_name='vip/vip_form.html'
    def form_valid(self, form):
        form.instance.user=self.request.user
        for i in punctuation:
            form.instance.title=form.instance.title.replace(i, '')
        form.instance.slug=form.instance.title.replace(' ', '-').lower()
        return super(vipsCreate, self).form_valid(form)
    
@login_required(login_url='login')
def profile(request,):
    page="Profile"
    user = request.user
    form = ProfileForm(instance=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile')
    context={'form':form, 'page':page}
    return render(request, 'vip/profile_form.html', context)




def confirmParticipation(request):
    return render (request, 'vip/confirm.html')


def participant(request, id):
    selected_vip=vip.objects.get(id=id)
    participants=selected_vip.participant.all
    participants=selected_vip.participant.order_by('-id')
    count=selected_vip.participant.count()
    return render(request, 'vip/participants.html', {'participants':participants, 'counts':count, 'vip':selected_vip})


class Contact(FormView):
    template_name = 'vip/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact-success')

    def form_valid(self, form):
        # Calls the custom send method
        form.send()
        return super().form_valid(form)

def contact_success(request):
    return render(request, 'vip/contact_success.html')

# uri = "mongodb+srv://bigdeal035:<password>@cluster0.wk8vay0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))

# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)
