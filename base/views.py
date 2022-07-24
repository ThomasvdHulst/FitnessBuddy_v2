from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q #Lets you use and/or for filter
from django.contrib.auth import authenticate, login, logout 
from .models import Room, Topic, Message, User, Exercise, Workout, BodyPart, OwnExercise, Statement
from .forms import ExerciseForm, RoomForm, UserForm, MyUserCreationForm

from itertools import chain
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
             login(request, user) #adds session in database
             return redirect('home')
        else:
             messages.error(request, 'Username OR password is not correct, please try again.')


    context = {'page':page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = user.email.lower()
            user.save()
            login(request, user)
            return redirect('home')
        elif any(char.isdigit() for char in request.POST.get('name')):
             messages.error(request, 'Please only use letters for your name.')
        elif len(request.POST.get('name')) < 2:
            messages.error(request, 'Please fill in a correct name.')
        elif len(request.POST.get('password1')) < 8:
            messages.error(request, 'Please create a password with atleast 8 characters.')
        elif request.POST.get('password1') != request.POST.get('password2'):
            messages.error(request, 'Please fill in the same passwords.')
        else:
            messages.error(request, 'Email/Username already taken.')

    return render(request, 'base/login_register.html', {'form':form})


def home(request):
    # q = request.GET.get('q') if request.GET.get('q') != None else ''

    # rooms = Room.objects.filter(
    #     Q(topic__name__icontains=q) | #icontains: look if a part of it matches, i makes in not capitalsensative
    #     Q(name__icontains=q) |
    #     Q(description__icontains=q)
    #     )

    # topics = Topic.objects.all()[0:5]
    # room_count = rooms.count()
    # room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    # context_old = {'rooms':rooms, 'topics':topics, 'room_count':room_count,
    #             'room_messages':room_messages}

    if request.user.is_authenticated:
        workouts = Workout.objects.filter(
            user=request.user, completed = 'YES'
            )[0:5]
        return render(request, 'base/home.html', {'workouts':workouts})
    else:
        return render(request, 'base/home.html', {})

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all() #Gives set of messages that are related
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room':room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    # user = User.objects.get(id=pk)
    # rooms = user.room_set.all()
    # room_messages = user.message_set.all()
    # topics = Topic.objects.all()
    # context = {'user':user, 'rooms':rooms, 'room_messages':room_messages, 'topics':topics}
    workouts = Workout.objects.filter(
        user=request.user, completed = 'YES'
        )[0:5]

    context ={'workouts':workouts}
    return render(request, 'base/profile.html', context)



@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name) #Lets you choose a created topic or create a new one

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect('home')

    context = {'form':form, 'topics':topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room) #Prefilled form 
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name) #Lets you choose a created topic or create a new one
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form':form, 'topics':topics, 'room':room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})

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

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains = q)
    return render(request, 'base/topics.html', {'topics': topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages':room_messages})




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
    ).last()
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
    statements = Statement.objects.all()

    context = {'statements':statements}
    return render(request, 'base/knowledge.html', context)