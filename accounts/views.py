from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import RegForm, UpdationForm
from django.contrib.auth import login,authenticate,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required,permission_required
from .models import RightsSupport,UserAccounts
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.contrib import messages
# Create your views here.

USER_URL = "/accounts/user/login/"
OWNER_URL = "/accounts/owner/login/"

def user_register_view(request):
    if request.method == "POST":
        form = RegForm(request.POST)
        if form.is_valid():
            tmp = form.save()
            user = UserAccounts.objects.get(id=tmp.id)
            content_type = ContentType.objects.get_for_model(RightsSupport)
            permission = Permission.objects.get(
                codename='user_rights',
                content_type=content_type,
            )
            user.user_permissions.add(permission)
            messages.success(request, 'User registration was successful!')
            return redirect(USER_URL)
        else:
            return render(request, 'accounts/register.html',{"form":form})
    else:
        form = RegForm()
        return render(request,"accounts/register.html",{"form":form})

def user_login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        check = authenticate(username=email,password=password)
        if check and not check.is_bus_owner:
            login(request,check)
            messages.success(request, 'Your are logged in successfully!')
            return redirect("/bus/user/main/")
        else:
            messages.error(request, 'username or password incorrect')
            return render(request ,"accounts/login.html",{"login_error_msg":"username or password incorrect"})

    else:
        return render(request ,"accounts/login.html")

def owner_register_view(request):
    if request.method == "POST":
        form = RegForm(request.POST)
        if form.is_valid():
            tmp = form.save(commit=False)
            tmp.is_bus_owner = True
            tmp.save()
            user = UserAccounts.objects.get(id=tmp.id)
            content_type = ContentType.objects.get_for_model(RightsSupport)
            permission = Permission.objects.get(
                codename='owner_rights',
                content_type=content_type,
            )
            user.user_permissions.add(permission)
            messages.success(request, 'Bus registration was successful!')
            return redirect(OWNER_URL)

        else:
            return render(request, 'accounts/register_owner.html',{"form":form})
    else:
        form = RegForm()
        return render(request,"accounts/register_owner.html",{"form":form})

def owner_login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        check = authenticate(username=email,password=password)
        if check and check.is_bus_owner:
            login(request, check)
            messages.success(request, 'Your are logged in successfully!')
            return redirect('/bus/owner/main/')
        else:
            messages.error(request, 'username or password incorrect')
            return render(request ,"accounts/login_bus.html",{"login_error_msg":"username or password incorrect"})

    else:
        return render(request ,"accounts/login_bus.html")

def edit_view(request):
    if request.method == "POST":
        form = UpdationForm(request.POST,instance=request.user)
        if form.is_valid():
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            if password1 and password2:
                if password1 == password1:
                    # u = UserAccounts.objects.get(email=request.user.email)
                    # u.set_password(password1)
                    request.user.set_password(password1)
                    update_session_auth_hash(request, request.user)
                    print("set")
                    # u.save()
                    form.save()
                    messages.success(request, 'User Details and Passwords Updated!')
                else:
                    messages.error(request, 'Password mismatch!')
                    return redirect("/accounts/edit/")
            else:
                form.save()
                messages.success(request, 'User Details Updated!')
            return redirect("/")
        else:
            return render(request, 'accounts/edit.html',{"form":form})
    else:
        form = UpdationForm(instance=request.user)
        return render(request,"accounts/edit.html",{"form":form})

@login_required(login_url=USER_URL)
def main_view(request):
    if request.user.is_bus_owner:
        return redirect('/bus/owner/main/')
    else:
        return redirect('/bus/user/main/')

def logout_view(request):
    logout(request)
    messages.info(request, 'Your are logged out !')
    return redirect(USER_URL)