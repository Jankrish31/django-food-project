from django.contrib.auth.models import User
from django import forms
from learnapp.models import UserDetails
from django_recaptcha.fields import ReCaptchaField

class Userform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','password']
        

class UserProfileform(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ['phone','address','street','city','zipcode','userpic']
    captcha = ReCaptchaField()
    
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ['phone','address','street','city','zipcode','userpic']

