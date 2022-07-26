from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class ShopItemSection(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class ShopItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    image = models.ImageField(null=True, blank=True)
    price = models.FloatField(null=True)
    section = models.ForeignKey(ShopItemSection, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class ShoppingCart(models.Model):
    name = models.CharField(max_length=100, null=True)
    items = models.ManyToManyField(ShopItem)

    def __str__(self):
        return self.name

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True, unique=True)
    is_email_verified = models.BooleanField(default=False)
    bio = models.TextField(null=True, blank=True)
    completed_knowledge_statement = models.BooleanField(default=False)
    shoppingcart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, null=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Statement(models.Model):
    name = models.CharField(max_length=100)
    completed = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name + " " + self.user.username

class BodyPart(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class OwnExercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    image = models.ImageField(null=True, blank=True)
    bodypart_trained = models.ForeignKey(BodyPart, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Exercise(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    image = models.ImageField(null=True, blank=True)
    bodypart_trained = models.ForeignKey(BodyPart, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Workout(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    exercise = models.ManyToManyField(Exercise)
    ownexercise = models.ManyToManyField(OwnExercise)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    completed = models.CharField(max_length=5, default='NO')

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

class EncTopic(models.Model):
    name = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.name

class EncItem(models.Model):
    name = models.CharField(max_length=100, null=True)
    body = models.TextField(null=True)
    topic = models.ForeignKey(EncTopic, on_delete=models.CASCADE, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name



