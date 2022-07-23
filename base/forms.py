from django.forms import ModelForm
from .models import Room, User, OwnExercise
from django.contrib.auth.forms import UserCreationForm  

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__' #Gives all fields
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']

class ExerciseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False
        self.fields['bodypart_trained'].required = True


    class Meta:
        model = OwnExercise
        fields = ['name', 'description', 'bodypart_trained']