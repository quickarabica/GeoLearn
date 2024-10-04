from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext,gettext_lazy as _
from .models import BlogPost,event1,event2,contact
class SignUpForm(UserCreationForm):
    password1=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(label="Confirmed Password",widget=forms.PasswordInput(attrs={"class":"form-control"}))

    class Meta:
        model=User
        fields=["username","first_name","last_name","email"]
        labels={"first_name":"First Name","last_name":"Last Name","email":"Email"}
        widgets={"username":forms.TextInput(attrs={"class":"form-control","size":60}),
        "first_name":forms.TextInput(attrs={"class":"form-control"}),
        "last_name":forms.TextInput(attrs={"class":"form-control"}),
        "email":forms.EmailInput(attrs={"class":"form-control"}),
                 }
        
class LogInForm(AuthenticationForm):
 username=UsernameField(widget=forms.TextInput(attrs={"autofocus":True,'class':"form-control","size":60}))
 password=forms.CharField(label=_("Password"),strip=False,widget=forms.PasswordInput(attrs={"autocomplete":'current-password','class':"form-control","size":60}))



class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image']
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class event1Form(forms.ModelForm):
    class Meta:
        model = event1
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
           
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }



class event2Form(forms.ModelForm):
    class Meta:
        model = event2
        fields = ['name', 'email']   
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
           
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }             


class contactForm(forms.ModelForm):
    class Meta:
        model = contact
        fields = ["message"]  
        labels={"message":"Your Message"}
        widgets = {
            
            
            'message': forms.TextInput(attrs={'class': 'form-control'}),
        }   

