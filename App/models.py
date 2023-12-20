# models.py
from django.db import models

class UserProfile(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Use a more secure method for passwords

class ResumeInfo(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    about_you = models.TextField()
    education = models.TextField()
    career = models.TextField()
    job_1_start = models.CharField(max_length=10, blank=True, null=True)
    job_1_end = models.CharField(max_length=10, blank=True, null=True)
    job_1_details = models.TextField(blank=True, null=True)
    job_2_start = models.CharField(max_length=10, blank=True, null=True)
    job_2_end = models.CharField(max_length=10, blank=True, null=True)
    job_2_details = models.TextField(blank=True, null=True)
    job_3_start = models.CharField(max_length=10, blank=True, null=True)
    job_3_end = models.CharField(max_length=10, blank=True, null=True)
    job_3_details = models.TextField(blank=True, null=True)
    references = models.TextField(blank=True, null=True)
