from django.db import models

class Users(models.Model):
    name = models.CharField(max_length=254)
    password = models.CharField(max_length=254)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        default_related_name = 'users'
    def __str__(self):
        return self.name

class Sessions(models.Model):
    token = models.CharField(max_length=254)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='sessions')

    class Meta:
        default_related_name = 'sessions'
    def __str__(self):
        return self.token