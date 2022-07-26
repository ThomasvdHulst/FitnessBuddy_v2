from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q #Lets you use and/or for filter
from django.contrib.auth import authenticate, login, logout 
from .models import User, Exercise, Workout, BodyPart, OwnExercise, Statement, EncItem, EncTopic
from .forms import ExerciseForm, UserForm, MyUserCreationForm

from itertools import chain

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
import threading

class EmailThread(threading.Thread): #Makes sure user doesnt have to wait long for response
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()
    

def send_activation_email(request, user):
    current_site = get_current_site(request)    #Gives domain
    email_subject = 'Activate your account'
    email_body = render_to_string('base/activate.html', {
        'user':user,
        'domain':current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)), 
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body, 
        from_email= settings.EMAIL_FROM_USER,
        to=[user.email]
         )

    EmailThread(email).start()

def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64)) 

        user = User.objects.get(pk=uid)
        
    except Exception as e:
        user=None
    
    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        login(request,user)
        messages.success(request, 'Email verified, welcome ' + user.username)
        return redirect(reverse('home'))

    return render(request, 'base/activate-failed.html', {"user":user})



# Create your views here.

def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            pass

        user = authenticate(request, email=email, password=password) 

        if user is not None:
            if not user.is_email_verified & user.is_staff == False:
                messages.success(request, 'Email is not verified.')
                return render(request, 'base/login_register.html', {'page':page})

            login(request, user) #adds session in database


            #ONLY USED FOR UPDATES IN STATEMENTS
            # adminstatements = Statement.objects.filter(
            #     Q(user='1')
            #     )

            # for statement in adminstatements:
            #     statement.pk = None
            #     statement.user = request.user
            #     statement.save()

            return redirect('home')
        else:
             messages.error(request, 'Email or password is not correct, please try again.')


    context = {'page':page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)

        username_taken = False
        for user in User.objects.all():
            if user.username == request.POST.get('username'):
                username_taken = True

        email_taken = False
        for user in User.objects.all():
            if user.email == request.POST.get('email'):
                email_taken = True

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = user.email.lower()
            user.save()

            adminstatements = Statement.objects.filter(
                Q(user='1')
                )


            for statement in adminstatements:
                statement.pk = None
                statement.user = user
                statement.save()


            send_activation_email(request, user)
            messages.success(request, 'An mail has been sent to your email-adress, please verify your account.')
            
            return redirect('login')
        elif any(char.isdigit() for char in request.POST.get('name')):
             messages.error(request, 'Please only use letters for your name.')
        elif len(request.POST.get('name')) < 2:
            messages.error(request, 'Please fill in a correct name.')
        elif len(request.POST.get('password1')) < 8:
            messages.error(request, 'Please create a password with atleast 8 characters.')
        elif request.POST.get('password1') != request.POST.get('password2'):
            messages.error(request, 'Please fill in the same passwords.')
        elif username_taken:
            messages.error(request, 'This username is already taken sadly, please choose another one!')
        elif email_taken:
            messages.error(request, 'There already exists an account with this email, please log in with this email or choose another one to create an account.')
        elif "@" in request.POST.get('email') == False:
            messages.error(request, 'Please fill in an correct email-adress.') 
        else:
            messages.error(request, 'Email/Username already taken.')

    return render(request, 'base/login_register.html', {'form':form})


def home(request):
    if request.user.is_authenticated:
        workouts = Workout.objects.filter(
            user=request.user, completed = 'YES'
            )[0:5]
        return render(request, 'base/home.html', {'workouts':workouts})
    else:
        return render(request, 'base/home.html', {})

def userProfile(request, pk):
    workouts = Workout.objects.filter(
        user=request.user, completed = 'YES'
        )[0:5]

    context ={'workouts':workouts}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)


    return render(request, 'base/update-user.html', {'form':form})


def exerciseLibrary(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    bodyparts = BodyPart.objects.all()

    exercises = Exercise.objects.filter(
        Q(name__icontains=q) | #icontains: look if a part of it matches, i makes in not capitalsensative
        Q(description__icontains=q) |
        Q(bodypart_trained__name__icontains=q)
        )

    ownexercises = OwnExercise.objects.filter(
        Q(user=request.user) &
        (Q(name__icontains=q) | #icontains: look if a part of it matches, i makes in not capitalsensative
        Q(description__icontains=q) |
        Q(bodypart_trained__name__icontains=q))
        )
        
    totalexercises = list(chain(exercises, ownexercises))

    context = {'exercises':exercises, 'bodyparts':bodyparts, 'ownexercises':ownexercises, 'totalexercises':totalexercises}
    return render(request, 'base/exercise_library.html', context)

@login_required(login_url='login')
def startWorkout(request):
    if request.method =='POST':
        workoutname = request.POST.get('workoutname') 
        workout = Workout(user=request.user, name=workoutname)
        workout.save()
        return redirect('workout')

    workouts = Workout.objects.filter(
        user=request.user, completed = 'YES'
        )[0:5]

    context = {'workouts':workouts}
    return render(request, 'base/startworkout.html', context)

@login_required(login_url='login')
def workout(request):
    workout = Workout.objects.filter(user=request.user).first()
    currentExercises = workout.exercise.all()
    currentOwnExercises = workout.ownexercise.all()

    cancelbtn = request.POST.get('cancelbtn')
    addNewExercisebtn = request.POST.get('addNewExercisebtn')
    addOwnNewExercisebtn = request.POST.get('addOwnNewExercisebtn')
    completebtn = request.POST.get('completebtn')

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    exercises = Exercise.objects.filter(
        Q(name__icontains=q) | #icontains: look if a part of it matches, i makes in not capitalsensative
        Q(description__icontains=q) |
        Q(bodypart_trained__name__icontains=q)
        )

    ownexercises = OwnExercise.objects.filter(
        Q(user=request.user) &
        (Q(name__icontains=q) | #icontains: look if a part of it matches, i makes in not capitalsensative
        Q(description__icontains=q) |
        Q(bodypart_trained__name__icontains=q))
        )

    if cancelbtn != None:
        workout.delete()
        return redirect('home')

    elif addNewExercisebtn != None:
        exerciseChosen = Exercise.objects.filter(id=addNewExercisebtn).first()
        workout.exercise.add(exerciseChosen)
        workout.save()
        currentExercises = workout.exercise.all()
        return redirect('workout')

    elif addOwnNewExercisebtn != None:
        exerciseChosen = OwnExercise.objects.filter(id=addOwnNewExercisebtn).first()
        workout.ownexercise.add(exerciseChosen)
        workout.save()
        currentOwnExercises = workout.ownexercise.all()
        return redirect('workout')

    elif completebtn != None:
        if workout.exercise.exists() or workout.ownexercise.exists():
            workout.completed = 'YES'
            workout.save()
            return redirect('workout-completed')
        
        else:
             messages.error(request, 'Please at a exercise before completing your workout.')

    context = {'workout':workout, 'exercises':exercises, 'currentExercises':currentExercises, 'ownexercises':ownexercises, 'currentOwnExercises':currentOwnExercises}
    return render(request, 'base/workout.html', context)

@login_required(login_url='login')
def workoutCompleted(request):
    workouts = Workout.objects.filter(
        Q(user=request.user) &
        Q(completed='YES')
    )
    
    lastWorkout = Workout.objects.filter(
        Q(user__exact=request.user) &
        Q(completed='YES')
    ).first()
    lastWorkoutExercises = lastWorkout.exercise.all()
    lastWorkoutOwnExercises = lastWorkout.ownexercise.all()

    numberOfWorkouts = workouts.count()

    context = {'numberOfWorkouts':numberOfWorkouts, 'lastWorkoutExercises':lastWorkoutExercises, 'lastWorkoutOwnExercises':lastWorkoutOwnExercises}
    return render(request, 'base/workout_completed.html', context)

@login_required(login_url='login')
def allWorkouts(request):
    workouts = Workout.objects.filter(
        Q(user=request.user) &
        Q(completed='YES')
    )

    context = {'workouts':workouts}
    return render(request, 'base/all_workouts.html', context)

@login_required(login_url='login')
def deleteWorkout(request, pk):
    workout = Workout.objects.get(id=pk)

    if request.user != workout.user:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        workout.delete()
        return redirect('all-workouts')
    return render(request, 'base/delete.html', {'obj':workout})

@login_required(login_url='login')
def createExercise(request):
    form = ExerciseForm()

    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.user = request.user
            exercise.save()
            messages.success(request, 'Exercise created!')
            return redirect('exercise-library')


    context ={'form':form}
    return render(request, 'base/create_exercise.html', context)

@login_required(login_url='login')
def knowledge(request):
    statements = Statement.objects.filter(
        Q(user=request.user)
        )

    saved = request.POST.get('save')

    if saved != None:
        for statement in statements:
            if request.POST.get("c" + str(statement.id)) == "clicked":
                statement.completed = True
            else:
                statement.completed = False
                    
            statement.save()
        request.user.completed_knowledge_statement = True
        request.user.save()

        messages.success(request, 'Well done! Lets gets working!')
        return render(request, 'base/knowledge.html', {'statements':statements})

    context = {'statements':statements}
    return render(request, 'base/knowledge.html', context)

def encyclopedia(request):
    items = EncItem.objects.all()
    topics = EncTopic.objects.all()

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    items = EncItem.objects.filter(
        Q(name__icontains=q) | #icontains: look if a part of it matches, i makes in not capitalsensative
        Q(topic__name__icontains=q)
        )

    workouts = Workout.objects.filter(
        user=request.user, completed = 'YES'
        )[0:5]

    context = {'items':items, 'topics':topics, 'workouts':workouts}
    return render(request, 'base/encyclopedia.html', context)

def viewEncItem(request, pk):
    item = EncItem.objects.get(id=pk)
    topics = EncTopic.objects.all()

    workouts = Workout.objects.filter(
        user=request.user, completed = 'YES'
        )[0:5]

    context = {'item':item, 'topics':topics, 'workouts':workouts}
    return render(request, 'base/view_enc_item.html', context)