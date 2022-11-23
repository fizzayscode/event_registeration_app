from contextlib import ContextDecorator
from multiprocessing import context
from urllib.request import Request
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import SubmissionForm,CustomUserCreation,UserForm
from .models import User,Event,Submission
from django.contrib.auth import login,logout, authenticate
from PIL import Image
from io import StringIO 
# from cStringIO import StringIO
# import Image



# Create your views here.
def login_page(request):
    page='login'
    # im submitting my email and password to the login so i have to get them here once i submit
    # by cathcing the name fields im able to store them in a local variable
    if request.method=='POST':
        email = request.POST['email']
        password = request.POST['password']
        # then the authenticate methd helps me check the database if i have a user with those credentails
        # and it returns an object so i store it in the user
        user = authenticate(request, email=email, password=password)
    # if the user was not found it returns a none object 
        if user is not None:
            # if its not none then django helps us beautifully witht the login and creates the session for us 
            # till the user logs out
            login(request, user)
            return redirect('index')

        else:
            return HttpResponse("User with this credentials was not found")


    context={'page':page}
    return render(request,'login_register.html',context)


def register_page(request):
    page='register'
    form = CustomUserCreation()

    if request.method=='POST':
        form = CustomUserCreation(request.POST)

        if form.is_valid():
            # helps return an user object or instance for further use i caught it and logged in the user
            user=form.save()

            login(request,user)
            return redirect('account-page')


    context={'page':page, 'form':form}
    return render(request, 'login_register.html',context)


def logout_page(request):
    logout(request)
    return redirect('login')


def index(request):
    # using filter because i dont want the admin to be
    #  rendered i dont to the admin to participate just only the users 
    users=User.objects.filter(is_participant=True)
    events=Event.objects.all()
    context={'users':users,
              'events':events}
    return render(request,'index.html', context)



def event_page(request, id):
    event=Event.objects.get(id=id)
    registered=False
    submitted=False
    submit_if_registered=False
    
    submit_id=Submission.objects.filter(participant=request.user,event=event)


    if request.user.is_authenticated:
        # im filtering the particular user-events based on this event if hes registered
        # in the  model i created a related name so i will be abe to backtrack my events from users
        # beacuse its a many to many field and i need the query set
        registered=request.user.events.filter(id=event.id).exists()

        # filtering based on the request.user and event if found the user has submitted already
        submitted=Submission.objects.filter(participant=request.user,event=event).exists()

    if not registered:
        submit_if_registered=True

    context={
        'event':event,
        'registered':registered,
        'submitted':submitted,
        'submit_if_registered':submit_if_registered,
        'submit_id':submit_id
    }
    return render(request,'eventpage.html',context)

# creating just like a modal that pops up if i click on register on the event_page
# im redirecting the user thats not logged in to the log in page
@login_required(login_url='login')
def register_confirm(request, id):
    event=get_object_or_404(Event, id=id)

    if request.method=="POST":
        # with django built in authenticatiom we can access the current user by just request.user 
        # because youve to be logged in so its getting it from the session
        event.participants.add(request.user)
        # passing dynamic values to take me back to the event page with that id 
        return redirect('event_page',id=event.id)
    context={'event':event}
    return render(request,'event_confirm.html', context)


def profile_page(request,id):
    user=User.objects.get(id=id)
    context={'user':user}
    return render(request,'profile.html',context)


@login_required(login_url='login')
def account_page(request):
    # getting the user from the session thats if he is logged in
    user=request.user
    return render(request,'account.html')


@login_required(login_url='login')
def edit_profile(request):
    user=request.user
    form= UserForm(instance=user)
    if request.method=='POST':
        # img=Image.open(request.FILES.get('avatar'))
        # newSize=(10,10)
        # img=img.resize(newSize)
        # request.FILES['avatar']=img
        # we have to pass in the files into the form also fo it parses it with the data 
        print("my file", request.FILES.get('avatar'))
        form =UserForm(request.POST,request.FILES,instance=user)


        if form.is_valid():
            form.save()
            return redirect('account-page')


    context={'form':form, 'user':user}
    return render(request, "edit-profile.html",context)



@login_required(login_url='login')
def submit_form(request,id):
    event=get_object_or_404(Event,id=id)
    user=request.user

    # the initial helps make the value default then we pass in the instacne we want to make default
    form = SubmissionForm()

    if request.method=='POST':
        # request.POST pass in all the data thats in the request body to be submitted
        form = SubmissionForm(request.POST)

        if form.is_valid():
            # dont save my from to the datatbase yet but create an object and return to f thats its only 
            # the decription the post is containing so id to add the events and participants manually before saving 
            f=form.save(commit=False)
            f.participant=user
            f.event=event
            f.save()

            return redirect('account-page')

    context={'event':event, 'form':form}
    return render(request,'submit_form.html',context)


@login_required(login_url='login')
def update_form(request,id):
    submission=Submission.objects.get(id=id)
   
    # if i have a user tyring to modify another persons work by puttin his id in the
    if request.user != submission.participant:
        return HttpResponse("you cant modify another persons work")

    # getting my form to be populated by using the instance the event 
    # description because i want to update it
    form=SubmissionForm(instance=submission)
    event=submission.event
    
    if request.method=='POST':
        # im getting what i posted from the request and updated my instance directly from that
        # if i didnt pass the instance to ,odify it will create a new object we want to make sure its
        # modifying the instance
        form = SubmissionForm(request.POST,instance=submission)
        if form.is_valid():
            form.save()
            return redirect('account-page')
    context={'form':form,'event':event}
    return render(request,'submit_form.html',context)
