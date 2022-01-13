from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager



class UserProfileManager(BaseUserManager):
    """Manager for user profile """
    def create_user(self,email,name,password=None):
        """Create a new user profile"""

        if not email:
            raise ValueError('Users must have a email adress')

        #to make second half of email adress to lower case
        email = self.normalize_email(email)
        user = self.model(email=email,name=name)

        user.set_password(password)
        #specify which database is using.to support multiple databases in future
        user.save(using=self._db)

        return user

    def create_superuser(self,email,name,password):
        """Create and save new superuser"""
        user = self.create_user(email,name,password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

        

class UserProfile(AbstractBaseUser,PermissionsMixin):
    """Databasemodel for users in the system"""
    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True) #tocheck user profile activated or not
    is_staff = models.BooleanField(default=False) #staff user for django admin acess

    #specify model manager
    objects = UserProfileManager()

    #overriding default username field to email

    USERNAME_FIELD = 'email'
    REQUIRED_FILEDS = ['name']

    def get_full_name(self):
        """Retrive full name of user"""
        return self.name 

    def get_short_name(self):
        """Retrive short name of user"""
        return self.name

    #string represntation of model 

    def __str__(self):
        """Return string representation of our user"""
        return self.email

