from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('department', views.department_dashboard, name='department_dashboard'),
    path('departments/<int:dept_id>/', views.department_details, name='department_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('add/', views.add_department, name='add_department'),
    path('update/<int:id>/', views.update_department, name='update_department'),
    path('delete/<int:id>/', views.delete_department, name='delete_department'),
    path('no_role/', views.no_role, name='no_role_page'),  
    path('forgot_password/',views.forgotpassword,name='forgotpassword'),
    path('resetpassword/<uidb64>/<token>/', views.resetpassword, name='resetpassword'),
    path('password_reset_done/', views.password_reset_done, name='passwordresetdone'),
    path('update-task-status/<int:assignment_id>/', views.update_task_status, name='update_task_status'),
    path('Admin_All_Sections/', views.all_section, name='Admin_All_Sections'),

]