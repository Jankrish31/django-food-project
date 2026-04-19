from django.shortcuts import render,redirect
from learnapp.forms import Userform,UserProfileform,UserUpdateForm,UserProfileUpdateForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from foods.models import FoodItems,Cart
from foods.forms import AddFoodForm
from learnapp.models import UserDetails

# Create your views here.
def registration(request):
    registered = False
    if request.method == 'POST':
       
        form1 = Userform(request.POST)
        form2 = UserProfileform(request.POST,request.FILES)
        
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            
            profile = form2.save(commit=False)
            profile.user = user  # connecting two models to save final data
            profile.save()
            registered = True
    else:
        form1=Userform()
        form2=UserProfileform()
    context = {
        'form1' :form1,
        'form2' :form2,
        'registered' :registered
        }
    return render(request,'registration.html',context)
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return redirect("home")
            else:
                return HttpResponse("User is not Active")
        else:
            return HttpResponse("Pls Check Your Crendenial..!")
        
    return render(request,"login.html",{})

@login_required(login_url='login')
def home(request):
    allfoods = FoodItems.objects.all()
    return render(request,'home.html',{'allfoods' : allfoods })



@login_required(login_url="login")
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url="login")
def userprofile(request):
    return render(request,'profile.html')

@login_required(login_url='login')
def userupdate(request):
    if request.method == 'POST':
        form= UserUpdateForm(request.POST,instance=request.user)
        form1 = UserProfileUpdateForm(request.POST,request.FILES,instance=request.user.userdetails)
    
        if form.is_valid() and form1.is_valid():
            user=form.save()
            user.save()

            profile = form1.save(commit=False)
            profile.user=user
            profile.save()
            return redirect("profile")
    else:
         form = UserUpdateForm(instance=request.user)
         form1 = UserProfileUpdateForm(instance=request.user.userdetails)
    context ={
        'form' : form,
        'form1' : form1
    }
    
    return render(request,'update.html',context)



def AllFoods(request):
    cat = request.GET.get('cat')
    fooditems = FoodItems.objects.all()

    user_type=None


    if request.user.is_authenticated:
        try:
            profile = UserDetails.objects.get(user=request.user)
            user_type = profile.user_type
        except:
            user_type=None

    return render(request, 'AllFoods.html', {
        'fooditems': fooditems,
        'cat':cat,
        'user_type':user_type
        })


def fooddetails(request):
    fooditem=FoodItems.objects.all()
    return render(request,'foodDetails.html',{"fooditem":fooditem})

def addnewfood(request):
    form= AddFoodForm()
    if request.method == 'POST':
        form =AddFoodForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('AllFoods')
        
    return render(request,"addnewfood.html" , {"form": form})










