from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('user/verification-pending/', views.verification_pending, name='verification_pending'),
    path('user/posts/', views.user_posts, name='my_posts'),
    path('user/activity/', views.user_activity, name='activity'),
    path('user/profile/', views.profile, name='profile'),
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('manager/users/', views.manage_users, name='manage_users'),
    path('manager/users/<int:user_id>/verify/', views.verify_user, name='verify_user'),
    path('manager/users/<int:user_id>/reject/', views.reject_user, name='reject_user'),
    path('manager/users/<int:user_id>/block/', views.block_user, name='block_user'),
    path('manager/activity/', views.activity_logs, name='activity_logs'),
    path('', views.dashboard, name='home'),
    path('create-managers/', views.create_managers, name='create_managers'),
]
