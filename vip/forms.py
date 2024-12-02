from django import forms
from .models import vip, myUser, Speaker, Participant
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.core.mail import send_mail


class UservipForm(forms.ModelForm):
    class Meta:
        model=vip
        fields='__all__'
        exclude=['slug', 'user','participant' ]

class MyUserRegistrationForm(UserCreationForm):
    class Meta:
        model=myUser
        fields= ['name', 'username', 'email', 'password1', 'password2' ]


class SpeakerRegistration(forms.ModelForm):
    class Meta:
        model=Speaker
        fields=['name', 'email', 'bio', 'image', 'vip_name'  ]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = myUser
        fields = [ 'name',  'email',  'image', 'phone', 'dob']

class ParticipantForm(forms.ModelForm):
    class Meta:
        model=Participant
        fields=['name', 'email', 'phone']


#Contact form
class ContactForm(forms.Form):

    name = forms.CharField(max_length=120, 
        widget=forms.TextInput(attrs={'placeholder': '*Your Full Name..'}))
    phone = forms.CharField(max_length=70, widget=forms.TextInput(attrs={'placeholder': '*Your Phone No...', }))
    email = forms.EmailField( widget=forms.EmailInput(attrs={'placeholder': '*Your email..'}))
    subject = forms.CharField( widget=forms.TextInput(attrs={'placeholder': '*Your subject..'}))
   
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': '*Your Message..'}))

    def get_info(self):
        """
        Method that returns formatted information
        :return: subject, msg
        """
        # Cleaned data
        cl_data = super().clean()

        name = cl_data.get('name').strip()
        from_email = cl_data.get('email')
        subject = cl_data.get('subject')

        msg = f'{name} with email {from_email} said:'
        msg += f'\n"{subject}"\n\n'
        msg += cl_data.get('message')

        return subject, msg

    def send(self):

        subject, msg = self.get_info()

        send_mail(
            subject=subject,
            message=msg,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.RECIPIENT_ADDRESS]
        )