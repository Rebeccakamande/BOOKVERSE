from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from django.contrib.auth import login,logout,authenticate
import re

def register_view(request):
    errors = {}

    if request.method == 'POST':
        full_name = request.POST.get("full_name", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        phone_number = request.POST.get("phone_number", "").strip()
        date_of_birth = request.POST.get("date_of_birth", "")
        password = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")
        profile_picture = request.FILES.get("profile_picture")

         # --- VALIDATIONS ---

        # Full name
        if not full_name:
            errors["full_name"] = "Full name is required."

        # Username
        if not username:
            errors["username"] = "Username is required."
        elif User.objects.filter(username=username).exists():
            errors["username"] = "Username already exists."

        # Email
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not email:
            errors["email"] = "Email is required."
        elif not re.match(email_regex, email):
            errors["email"] = "Enter a valid email address."
        elif User.objects.filter(email=email).exists():
            errors["email"] = "Email already registered."

        # Phone number
        if not phone_number or not phone_number.isdigit() or len(phone_number) != 10:
            errors["phone_number"] = "Enter a valid 10-digit phone number."

        # Date of birth
        if not date_of_birth:
            errors["date_of_birth"] = "Date of birth is required."

        # Passwords
        if not password:
            errors["password"] = "Password is required."
        elif len(password) < 6:
            errors["password"] = "Password must be at least 6 characters."
        if password != password2:
            errors["password"] = "Passwords do not match."     

        # create user
        if not errors:
            user = User.objects.create_user(
                full_name=full_name,
                username=username,
                email=email,
                phone_number=phone_number,
                date_of_birth=date_of_birth,
                profile_picture=profile_picture,
                password=password
            )

            messages.success(request, "Account created successfully")
            return redirect('login')

    return render(request, 'accounts/registrationForm.html', {"errors": errors})

# Login 
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')

        #Check if the email exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid email or Password")
            return render(request, 'acconts/loginForm.html')
        
        user = authenticate(request, username=user.username, password1=password1)

        if user is not None:
            if user.is_blocked:
                messages.error(request, "Your account has been blocked")
                return render(request, 'acconts/loginForm.html')
            
            login(request, user)
            messages.success(request, "Login Successfull")
            # return redirect("home")

    return render(request, 'accounts/loginForm.html')