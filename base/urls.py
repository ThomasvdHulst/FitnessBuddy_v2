from django.urls import URLPattern, path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('update-user/', views.updateUser, name="update-user"),

    path('exercise-library', views.exerciseLibrary, name="exercise-library"),
    path('start-workout', views.startWorkout, name="start-workout"),
    path('workout', views.workout, name="workout"),
    path('workout-completed', views.workoutCompleted, name="workout-completed"),
    path('all-workouts', views.allWorkouts, name="all-workouts"),
    path('delete-workout/<str:pk>/', views.deleteWorkout, name="delete-workout"),
    path('create-exercise', views.createExercise, name="create-exercise"),
    path('knowledge', views.knowledge, name="knowledge"),

    path('activate-user/<uidb64>/<token>', views.activate_user, name='activate'),
]