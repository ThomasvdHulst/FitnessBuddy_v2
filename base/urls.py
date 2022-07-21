from django.urls import URLPattern, path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    path('update-user/', views.updateUser, name="update-user"),

    path('topics/', views.topicsPage, name="topics"),

    path('activity/', views.activityPage, name="activity"),

    path('exercise-library', views.exerciseLibrary, name="exercise-library"),
    path('start-workout', views.startWorkout, name="start-workout"),
    path('workout', views.workout, name="workout"),
    path('workout-completed', views.workoutCompleted, name="workout-completed"),
    path('all-workouts', views.allWorkouts, name="all-workouts"),
    path('delete-workout/<str:pk>/', views.deleteWorkout, name="delete-workout"),
]