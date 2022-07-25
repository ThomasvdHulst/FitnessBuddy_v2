from django.contrib import admin

# Register your models here.
from .models import User, Exercise, Workout, BodyPart, OwnExercise, Statement

admin.site.register(User)
admin.site.register(Exercise)
admin.site.register(Workout)
admin.site.register(BodyPart)
admin.site.register(OwnExercise)
admin.site.register(Statement)