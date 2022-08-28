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
    path('encyclopedia', views.encyclopedia, name="encyclopedia"),
    path('view-enc-item/<str:pk>/', views.viewEncItem, name="view-enc-item"),
    path('shop', views.shop, name="shop"),
    path('view-shop-item/<str:pk>/', views.viewShopItem, name="view-shop-item"),
    path('shopping-cart', views.shoppingCart, name="shopping-cart"),
    path('delete-shopitem/<str:pk>/', views.deleteShopItem, name="delete-shopitem"),

    path('activate-user/<uidb64>/<token>', views.activate_user, name='activate'),
]