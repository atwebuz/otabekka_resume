# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile, ResumeInfo
import hashlib

def index(request):
    return render(request, "index.html")

def login(request):
    if request.method == "POST":
        username = request.POST.get("username").strip().lower()
        password = request.POST.get("password")

        try:
            user = UserProfile.objects.get(username=username)
            if hashlib.sha512(password.encode()).hexdigest() == user.password:
                request.session["user"] = {
                    "id": user.id,
                    "username": user.username
                }
                return redirect("App:index")
            else:
                raise UserProfile.DoesNotExist
        except UserProfile.DoesNotExist:
            messages.add_message(request, messages.INFO, "You have supplied invalid login credentials, please try again!", "danger")
            return redirect("App:login")

    return render(request, "login.html")

def register(request):
    if request.method == "POST":
        username = request.POST.get("username").strip().lower()
        email = request.POST.get("email").strip().lower()
        password = request.POST.get("password")

        try:
            UserProfile.objects.get(username=username)
            messages.add_message(request, messages.INFO, 'User already exists with that username.')
            return redirect("App:register")
        except UserProfile.DoesNotExist:
            user = UserProfile.objects.create(
                username=username,
                email=email,
                password=hashlib.sha512(password.encode()).hexdigest()
            )
            messages.add_message(request, messages.INFO, 'Registration successful.')
            return redirect("App:login")

    return render(request, "register.html")

def create_resume(request):
    if request.method == "POST":
        try:
            username = request.session["user"]["username"]
        except KeyError:
            messages.add_message(request, messages.INFO, 'User not logged in.')
            return redirect("App:login")

        # Retrieve form data
        full_name = request.POST.get("name")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        about_you = request.POST.get("about")
        education = request.POST.get("education")
        career = request.POST.get("career")
        job_1_start = request.POST.get("job-1__start")
        job_1_end = request.POST.get("job-1__end")
        job_1_details = request.POST.get("job-1__details")
        job_2_start = request.POST.get("job-2__start")
        job_2_end = request.POST.get("job-2__end")
        job_2_details = request.POST.get("job-2__details")
        job_3_start = request.POST.get("job-3__start")
        job_3_end = request.POST.get("job-3__end")
        job_3_details = request.POST.get("job-3__details")
        references = request.POST.get("references")

        user_profile = UserProfile.objects.get(username=username)
        resume, created = ResumeInfo.objects.get_or_create(user=user_profile)

        # Update resume info
        resume.full_name = full_name
        resume.address = address
        resume.phone = phone
        resume.email = email
        resume.about_you = about_you
        resume.education = education
        resume.career = career
        resume.job_1_start = job_1_start
        resume.job_1_end = job_1_end
        resume.job_1_details = job_1_details
        resume.job_2_start = job_2_start
        resume.job_2_end = job_2_end
        resume.job_2_details = job_2_details
        resume.job_3_start = job_3_start
        resume.job_3_end = job_3_end
        resume.job_3_details = job_3_details
        resume.references = references
        resume.save()

        messages.add_message(request, messages.INFO, 'Resume Info Saved Successfully. Download Resume Now')
        return redirect("App:resume")

    else:
        try:
            user_profile = UserProfile.objects.get(username=request.session["user"]["username"])
            resume_info, created = ResumeInfo.objects.get_or_create(user=user_profile)
            context = {"resume_info": resume_info}
            return render(request, "create-resume.html", context)
        except UserProfile.DoesNotExist:
            return render(request, "create-resume.html")

def resume(request):
    try:
        user_profile = UserProfile.objects.get(username=request.session["user"]["username"])
        resume_info, created = ResumeInfo.objects.get_or_create(user=user_profile)
        context = {"resume_info": resume_info}
        return render(request, "resume.html", context)
    except UserProfile.DoesNotExist:
        return render(request, "resume.html")
