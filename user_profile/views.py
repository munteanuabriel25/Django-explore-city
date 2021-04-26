from django.shortcuts import render,reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.views import View


from .forms import UserUpdateForm, UserProfileUpdateForm, UserLoginForm,UserRegisterForm
import blog

# Create your views here.





def update_user_profile(request,username):
    if request.method=='POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)

        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # messages.success(request, 'Your profile details has been updated')
            return HttpResponseRedirect(reverse("pages:user:user-profile",args=[str(username)]))

    else:
        user_form = UserUpdateForm(instance=request.user)
        post_form = blog.forms.PostCreateForm()
        profile_form = UserProfileUpdateForm(instance=request.user.userprofile)
  
    context = {'user_form':user_form,
               "profile_form":profile_form,
               "post_form":post_form,
               }
    return render(request, 'user_profile/user_profile.html', context)


def new_post(request, username):
    if request.method=="POST":
        post_form = blog.forms.PostCreateForm(request.POST,request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            if request.user.is_authenticated:
                user = User.objects.get(username=username)
                post.user = user
                post.save()
                post_form.save_m2m()

            return HttpResponseRedirect(reverse("pages:user:user-profile", args=[str(username)]))

    
    

def user_login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user != None:
                login(request, user)
                # messages.success(request, 'Your are loged in now')
                return HttpResponseRedirect(reverse('pages:home-view'))
            else:
                form = UserLoginForm()
                errors = "Username or password wrong"
                return render(request, 'user_profile/login.html', {"form": form, "errors": errors})
        else:
            return render(request, 'user_profile/login.html', {"form": form})
    
    else:
        form = UserLoginForm()
    return render(request, 'user_profile/login.html', {"form": form})

def user_logout_view(request):
    logout(request)
    # messages.success(request, 'Your are log out now')
    return HttpResponseRedirect(reverse('pages:home-view'))


def user_register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Your profile was created, log in now.')
            return HttpResponseRedirect(reverse("pages:home-view"))
        else:
            return render(request, 'user_profile/register.html', {"form": form})
    
    else:
        form = UserRegisterForm()
    
    return render(request, 'user_profile/register.html', {"form": form})



        
    