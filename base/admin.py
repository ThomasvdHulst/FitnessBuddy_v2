from django.contrib import admin

# Register your models here.
from .models import User, Exercise, Workout, BodyPart, OwnExercise, Statement, EncItem, EncTopic, ShopItem, ShopItemSection, ShoppingCart

admin.site.register(User)
admin.site.register(Exercise)
admin.site.register(Workout)
admin.site.register(BodyPart)
admin.site.register(OwnExercise)
admin.site.register(Statement)
admin.site.register(EncTopic)
admin.site.register(EncItem)
admin.site.register(ShopItem)
admin.site.register(ShopItemSection)
admin.site.register(ShoppingCart)