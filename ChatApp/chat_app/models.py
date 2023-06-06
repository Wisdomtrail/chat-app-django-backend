from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, email, phone_number='', password=None):
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            phone_number=phone_number
        )
        if password:
            user.set_password(password)

        user.save(using=self._db)
        return user


class ChatMessage(models.Model):
    sender = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey('User', on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'chat_app'


class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=100, blank=True, unique=True)
    inbox = models.CharField(max_length=10000, blank=True)
    chats = models.ManyToManyField('self', through='ChatMessage', symmetrical=False, related_name='chat_users')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
