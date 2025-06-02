import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from core.storage_backends import MediaStorage

class OrganizationManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Username is required')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        # This will just behave like a regular user creator
        return self.create_user(username, password, **extra_fields)

class Organization(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    # logo = models.ImageField(upload_to='logos/', blank=True, null=True)

    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    objects = OrganizationManager()

    def __str__(self):
        return self.name

    # ✅ These methods are required for Django Admin compatibility
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Employee(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Use custom S3 storage for profile picture
    profile_pic = models.ImageField(
        storage=MediaStorage(),  # This ensures it saves in `media/employees/`
        upload_to='employees/',
        blank=True,
        null=True
    )

    name = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=20)
    email = models.EmailField()
    short_intro = models.TextField()
    designation = models.CharField(max_length=255)
    linkedin_url = models.URLField()
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, default='O+')
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

