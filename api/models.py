from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.base import Model
from django.db.models.fields import CharField
from django.db.models.fields.files import ImageField
from django.http import request
import datetime
# from dateutil.relativedelta import *
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email,FirstName=None,LastName=None, phone=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError('Users must have a valid email')
        if not phone:
            raise ValueError('Users must have a valid phone number')
        if not password:
            raise ValueError("You must enter a password")

        email = self.normalize_email(email)
        user_obj = self.model(email=email)
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.FirstName = FirstName
        user_obj.LastName = LastName
        user_obj.phone = phone
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email,FirstName=None,LastName=None, phone=None, password=None):
        user = self.create_user(
            email,FirstName=FirstName,LastName=LastName, phone=phone, password=password, is_staff=True)
        return user

    def create_superuser(self, email,FirstName=None,LastName=None, phone=None, password=None):
        user = self.create_user(email,FirstName='0787018257',LastName='0787018257', phone='0787018234',
                                password=password, is_staff=True, is_admin=True)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    FirstName=models.CharField(max_length=255,  null=True, blank=True)
    LastName=models.CharField(max_length=255,  null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(
        max_length=255, unique=True, null=True, blank=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


class Installment(models.Model):
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, null=True, blank=True)
    Amount = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.user.FirstName + ' ' + self.user.LastName+' ' + self.Amount

class requestLoan(models.Model):
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, null=True, blank=True)
    Amount = models.CharField(max_length=255, null=True, blank=True)
    Sponsor1 = models.CharField(max_length=255, null=True, blank=True)
    Sponsor2 = models.CharField(max_length=255, null=True, blank=True)
    Approve = models.BooleanField(default=False)
    Request_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.user.phone + self.Amount


class loanPayment(models.Model):
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, null=True, blank=True)
    Amount = models.CharField(max_length=255, null=True, blank=True)
    Pay_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.user.FirstName + ' ' + self.user.LastName+' ' + self.Amount