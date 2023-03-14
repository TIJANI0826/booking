from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
User = get_user_model()
from . models import *
from django.contrib.auth.forms import UserCreationForm

GENDER_CHOICE =[

('Male','Male'),('Female','Female' )

]

GYM_REASON =[

('Build Body','Build Body'),
('Flat Tommy','Flat Tommy' ),
('Reduce Weight','Reduce Weight'),
('Hips','Hips'),

]


# Login Form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=250)
    password = forms.CharField(widget=forms.PasswordInput)
    remember = forms.BooleanField()
    


class UserRegistration(UserCreationForm):
   class Meta():
    model = User
    fields = [
        'username',
        'first_name',
        'last_name',
        'email',
        'phone',
        'address',
        'picture',
        'password1',
        'password2'
        ]

    
    def clean_password2(self):
      password = self.cleaned_data.get('password')
      password1 = self.cleaned_data.get('password1')
      if password and password1 and password != password:
        raise forms.ValidationError('Password MistMatch')
      return password1

    def save(self, commit=True):
      user = super(UserRegistration, self).save(commit=False)
      user.set_password(self.cleaned_data['password'])
      if commit:
        user.save()
      return user

     
class UserChangeForm(UserChangeForm):
    """Form to edit a user from admin"""

    class Meta:
        """Meta Class"""
        model = User
        fields = [
          'first_name',
          'last_name',
          'email','phone',
          'address',
          'picture',
          'password',
                              
          ]

""" BOOKING FOR HALL """
class HallBooking(forms.ModelForm):
    datetimeoptions = {
    'format':'dd/mm/yy HH:ii P',
    'autoclose':True
    # 'showMeridian':True
      
    }

    class Meta(): 
      model = Package
      exclude = ['is_available', 'service', 'is_approved']

      # widgets = {
      #  'start_date':forms.DateWidget()
      #  }
       


        	

#MEMBER REGISTRATION

class RegMember(forms.ModelForm):
    
    class Meta():
        model = Members
        exclude = ['barcode']
        widgets ={
            'start_date':forms.widgets.SelectDateWidget(),
            'gender':forms.widgets.RadioSelect( choices=GENDER_CHOICE),
            'exp_date':forms.widgets.SelectDateWidget(),
            'date_of_birth':forms.widgets.SelectDateWidget(),
            'date_of_birth':forms.widgets.SelectDateWidget(),
            'reason_for_registering':forms.widgets.CheckboxSelectMultiple(choices=GYM_REASON),
        }
         

class EditBookedTicket(forms.ModelForm):
    class Meta():
        model = TicketNumber
        fields = ['expired']


class RegLaundry(forms.ModelForm):
    class Meta():
        model = Laundry
        fields = '__all__'


        
