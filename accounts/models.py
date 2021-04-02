from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    """
    Override user model manager.
    """
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_superuser=False, is_previously_logged_in=False):
        """
        Take email, password, and create user.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')
        user_obj = self.model(email=self.normalize_email(email))
        user_obj.set_password(password)
        user_obj.is_active = is_active
        user_obj.is_staff_user = is_staff
        user_obj.is_superuser = is_superuser
        user_obj.previously_logged_in = is_previously_logged_in
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password=None):
        """
        Take email and password, and create staffuser.
        """
        user = self.create_user(email, password=password, is_staff=True)    
        return user

    def create_superuser(self, email, password=None):
        """
        Take email and password, and create superuser.
        """
        user = self.create_user(email, password=password, is_staff=True, is_superuser=True)    
        return user


class User(AbstractBaseUser):
    """
    User model.
    """
    email = models.EmailField(max_length=64, unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True) # can login
    is_staff_user = models.BooleanField(default=False) # staff user non superuser
    is_superuser = models.BooleanField(default=False) # superuser
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # USERNAME_FIELD and password are required by default.

    previously_logged_in = models.BooleanField(default=False)

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email  

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_staff_user   

    @property
    def is_previously_logged_in(self):
        return self.previously_logged_in