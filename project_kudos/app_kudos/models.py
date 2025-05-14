from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

class Organization(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

'''
    This is so that admin can modify the weekly kudos limit in future
'''
class KudoConfig(models.Model):
    weekly_kudos_limit = models.PositiveIntegerField(default=3)

    def __str__(self):
        return f"Weekly Kudos Limit: {self.weekly_kudos_limit}"
    
'''
    This is a custom super user creation management function
    Since user model has organization which is not null
    We are custom adding organization during creation of superuser
'''
class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        if not extra_fields.get("organization"):
            first_org = Organization.objects.first()
            if not first_org:
                raise ValueError("No organizations available. Please create one first.")
            extra_fields["organization"] = first_org

        return super().create_superuser(username, email, password, **extra_fields)

'''
    Inheriting all the fields from django.contrib.auth.models
'''
class User(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="users")

    objects = CustomUserManager()

    def __str__(self):
        return self.username

class Kudo(models.Model):
    from_user = models.ForeignKey(User, related_name="given_kudos", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="received_kudos", on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Kudos from {self.from_user} to {self.to_user}"