from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, full_name, password):
        if not phone_number:
            raise ValueError('The user must have a phone number')
        
        if not email:
            raise ValueError('The user must have an email')
        
        if not full_name:
            raise ValueError('The user must have an full name')
        
        user = self.model(phone_number=phone_number, email=self.normalize_email(email), full_name=full_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, full_name, password):
        user = self.create_user(phone_number, email, full_name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'full_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class OTPcode(models.Model):
    phone_number = models.CharField(max_length=11)
    code = models.SmallIntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}, {}, {}'.format(self.phone_number, self.code, self.created)
