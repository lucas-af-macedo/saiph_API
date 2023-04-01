from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Users(models.Model):
    name = models.CharField(max_length=254)
    password = models.CharField(max_length=254)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'password', 'USERNAME_FIELD']

    @property
    def is_anonymous(self):
        return not self.is_authenticated
    
    @property
    def is_authenticated(self):
        if self.is_active:
            return True
        else:
            return False
    
    def __str__(self):
        a = {'id': self.id, 'name':self.name}
        return self.name

class Teste(models.Model):
    oi = models.CharField(max_length=30)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='teste')

    class Meta:
        default_related_name = 'teste'
    def __str__(self):
        return self.oi