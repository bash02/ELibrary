from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth import get_user_model

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True, null=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    student_id = models.CharField(max_length=255, blank=True, null=True)  # Student ID
    faculty = models.CharField(max_length=255, blank=True, null=True)  # Faculty
    department = models.CharField(max_length=255, blank=True, null=True)  # Department
    student_category = models.CharField(max_length=50, choices=[
        ('undergraduate', 'Undergraduate'),
        ('postgraduate', 'Postgraduate'),
        ('masters', 'Masters'),
        ('phd', 'PhD'),
    ], blank=True, null=True)  # Student Category (Undergraduate, Postgraduate, etc.)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone', 'student_id', 'faculty', 'department', 'student_category', 'is_active', 'is_staff', 'is_superuser']  

    objects = UserManager()

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=255)

    def __str__(self):
        return self.display_name

class Subject(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=255)

    def __str__(self):
        return self.display_name

class EBook(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    upload_file = models.FileField(upload_to='ebook/files/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='ebook/thumbnails/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)  # admin-only approval

    class Meta:
        permissions = [
            ("can_create_ebook", "Can create ebook"),
        ]

    def __str__(self):
        return self.title

class EJournal(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    year = models.IntegerField(null=True)
    upload_file = models.FileField(upload_to='ejournal/files/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='ejournal/thumbnails/', blank=True, null=True)
    approved = models.BooleanField(default=False)  # admin-only approval
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Resource(models.Model):
    title = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to="resources/thumbnails/")
    url = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)  # admin-only approval
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.category.display_name})"

class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to='newspaper/thumbnails/', blank=True, null=True)
    approved = models.BooleanField(default=False)  # admin-only approval
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    url = models.URLField()

    def __str__(self):
        return self.title

class BorrowBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowed_books')
    book_title = models.CharField(max_length=255)  # Manual title input
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} borrowed "{self.book_title}"'

class IDCard(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='id_card')
    id_number = models.CharField(max_length=255, unique=True)  # Student ID
    faculty = models.CharField(max_length=255)  # Faculty
    department = models.CharField(max_length=255)  # Department
    student_category = models.CharField(max_length=50)  # Undergraduate, Postgraduate, etc.
    issued_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(null=True)

    def __str__(self):
        return f"ID Card for {self.user.username}"

    def get_card_details(self):
        return {
            "name": self.user.get_full_name(),
            "student_id": self.id_number,
            "faculty": self.faculty,
            "department": self.department,
            "student_category": self.student_category,
            "issued_date": self.issued_date,
            "expiry_date": self.expiry_date,
        }



