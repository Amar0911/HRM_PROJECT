from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Department
from .forms import DepartmentForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from roles.models import Role, UserRole



def index(request):
    return render(request, 'core/index.html')

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists!")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered!")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

        else:
            messages.error(request, "Passwords do not match!")

    return render(request, 'core/register.html')



def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            if user.is_staff:
                return redirect('department_dashboard')
            user_role = UserRole.objects.filter(user=user).first()
            if user_role:
                return redirect('user_dashboard')
            else:
                messages.warning(request, "No role assigned. Please contact the admin.")
                return redirect('no_role_page')  # Redirects to no_role.html
        else:
            messages.error(request, "Invalid username or password!")
    
    return render(request, 'core/login.html')


def user_logout(request):
    logout(request)
    return redirect('index')



@login_required
def user_dashboard(request):
    # Check if the user has an assigned role
    user_role = UserRole.objects.filter(user=request.user).first()

    if not user_role:
        # If no role is assigned, render a page informing the user
        return render(request, 'core/no_role.html', {'message': "No role assigned. Please contact the admin."})

    # Fetch user permissions if a role exists
    user_permissions = user_role.permissions.all()
    return render(request, 'core/user_dashboard.html', {'user_role': user_role, 'user_permissions': user_permissions})



# Dashboard View
def department_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect('index')
    departments = Department.objects.filter(status=True)
    return render(request, 'core/dashboard.html', {'departments': departments})



# Create Department
def add_department(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect('index')  # Redirect if the user is not staff

    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()  # Directly save the department without checking existence
            messages.success(request, "Department added successfully!")
            return redirect('department_dashboard')
    else:
        form = DepartmentForm()

    return render(request, 'core/add_department.html', {'form': form})



# Update Department
def update_department(request, id):
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect('index')

    department = get_object_or_404(Department, id=id)
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, "Department updated successfully!")
            return redirect('department_dashboard')

    else:
        form = DepartmentForm(instance=department)

    return render(request, 'core/update_department.html', {'form': form, 'department': department})



# Soft Delete Department (Set Status to False)
def delete_department(request, id):
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect('index')

    department = get_object_or_404(Department, id=id)

    if request.method == "POST":
        department.status = False  # Soft delete
        department.save()
        messages.success(request, "Department deactivated successfully!")
        return redirect('department_dashboard')

    return render(request, 'core/confirm_delete.html', {'department': department})




def no_role(request):
    return render(request, 'core/no_role.html', {'message': "No role assigned. Please contact the admin."})



#=======================================================================================================

#================ Forgot Password ======================

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.http import HttpResponse

def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(f'/resetpassword/{uidb64}/{token}/')           
            send_mail(
                'Password Reset Link',
                f'Click the following link to reset your password: {reset_url}',
                'movievistafilm@gmail.com', 
                [email],
                fail_silently=False,
            )
            return redirect('passwordresetdone')
        else:
            messages.success(request,'Please enter valid email address')
    return render(request, 'core/forgotpassword.html')                                        
    

def resetpassword(request, uidb64, token):
    if request.method == 'POST':
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
                if default_token_generator.check_token(user, token):
                    user.set_password(password)
                    user.save()
                    return redirect('passwordresetdone')
                else:
                    return HttpResponse('Token is invalid', status=400)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return HttpResponse('Invalid link', status=400)
        else:
            return HttpResponse('Passwords do not match', status=400)
    return render(request, 'core/resetpassword.html')

def password_reset_done(request):
    return render(request, 'core/password_reset_done.html')