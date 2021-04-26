from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField( required=True, widget=forms.EmailInput(attrs={"class": "input", "placeholder":"Enter your email"}))
    
    class Meta:
        model = User
        fields= ['username','email','password1','password2']
     
        widgets = {
            "username": forms.TextInput(attrs={"class": "input","placeholder":"Enter your username"}),
        }

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs["placeholder"] = "Enter a password"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirm password"
        self.fields["password1"].widget.attrs["class"] = "input"
        self.fields["password2"].widget.attrs["class"] = "input"
        
        
    def clean_email(self):
        data=self.cleaned_data.get("email")
        query = User.objects.filter(email=data)
        if query:
            raise forms.ValidationError("Allready have an account with same email")
        return data
    
    def clean_username(self):
        data=self.cleaned_data.get("username")
        data=data.lower()
        query = User.objects.filter(username=data)
        if query:
            raise forms.ValidationError("Allready have an account with same username")
        return data
    
class UserLoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "input","placeholder":"Enter your username"}))
    password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={"class": "input","placeholder":"Enter your password"}))
    
    
    
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "input-prof", "placeholder": "Enter your email"}))
    class Meta:
        model = User
        fields = ['username', 'email']
        
        widgets = {
            "username": forms.TextInput(attrs={"class": "input-prof", "placeholder": "Enter your username"}),
        }
        
class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields =['name', 'picture','facebook','instagram','blog_url','description']
        widgets = {
            "name": forms.TextInput(attrs={"class": "input-prof", "placeholder": "Enter your username"}),
            "picture": forms.FileInput(attrs={"class": "input-prof", "placeholder": "Enter your username"}),
            "facebook": forms.TextInput(attrs={"class": "input-prof", "placeholder": "Enter your username"}),
            "instagram": forms.TextInput(attrs={"class": "input-prof", "placeholder": "Enter your username"}),
            "blog_url": forms.URLInput(attrs={"class": "input-prof", "placeholder": "Enter your username"}),
            "description": forms.Textarea(attrs={"class": "input-prof", "placeholder": "Enter a short description about you","rows":4,'resize':'none'}),
        }


        