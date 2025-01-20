from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Department
from .forms import DepartmentForm
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                messages.success(request, 'Login successful. Welcome to the Dashboard!')
                return redirect('dashboard')  
            else:
                messages.error(request, 'Only admins can access the dashboard.')
                return redirect('login')  
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'core/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have logged out successfully.')
    return redirect('login')  


@login_required
def dashboard(request):
    if not request.user.is_superuser:
        messages.error(request, 'Access restricted to administrators.')
        return redirect('login')
    departments = Department.objects.filter(status=True)
    return render(request, 'core/home.html', {'departments': departments})

@login_required
def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department added successfully!')
            return redirect('add_department')
        else:
            messages.error(request, 'There was an error adding the department.')
    else:
        form = DepartmentForm()
    return render(request, 'core/add_department.html', {'form': form})

@login_required
def delete_department(request, id):
    department = get_object_or_404(Department, pk=id)
    if request.method == 'POST':
        department.status = False
        department.save()
        messages.success(request, f'Department "{department.Dept_Name}" deactivated successfully.')
        return redirect('dashboard')
    return render(request, 'core/confirm_delete.html', {'department': department})

@login_required
def update_department(request, id):
    department = get_object_or_404(Department, pk=id)
    form = DepartmentForm(request.POST or None, instance=department)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Department "{department.Dept_Name}" updated successfully.')
        return redirect('dashboard')
    return render(request, 'core/update.html', {'form': form})