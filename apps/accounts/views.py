from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth import get_user_model

from .forms import SignUpForm, LoginForm, UserManagementForm
from .models import ActivityLog
from apps.posts.models import Post

User = get_user_model()


def is_manager(user):
    return user.is_authenticated and user.role == 'manager'


def is_verified(user):
    return user.is_authenticated and user.status == 'verified'


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@require_http_methods(["GET", "POST"])
def signup(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            ActivityLog.objects.create(
                user=user,
                action='signup',
                ip_address=get_client_ip(request),
            )
            messages.success(request, 'Account created successfully! Please wait for manager verification.')
            return redirect('accounts:login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = SignUpForm()

    return render(request, 'auth/signup.html', {'form': form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)

            if user is not None:
                if not user.is_active:
                    messages.error(request, 'Your account has been deactivated.')
                    return redirect('accounts:login')

                login(request, user)
                user.is_online = True
                user.last_seen = timezone.now()
                user.save(update_fields=['is_online', 'last_seen'])

                ActivityLog.objects.create(
                    user=user,
                    action='login',
                    ip_address=get_client_ip(request),
                )

                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('accounts:dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', {'form': form})


@login_required
@require_http_methods(["POST"])
def logout_view(request):
    user = request.user
    ActivityLog.objects.create(
        user=user,
        action='logout',
        ip_address=get_client_ip(request),
    )

    user.is_online = False
    user.save(update_fields=['is_online'])

    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('accounts:login')


@login_required
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.user.role == 'manager':
        return redirect('accounts:manager_dashboard')
    elif request.user.status != 'verified':
        return redirect('accounts:verification_pending')

    return redirect('accounts:user_dashboard')


@login_required
def user_dashboard(request):
    if not is_verified(request.user):
        return redirect('accounts:verification_pending')

    available_posts = Post.objects.filter(
        status='available',
        is_deleted=False
    ).prefetch_related('images')

    claimed_posts = Post.objects.filter(
        claimed_by=request.user,
        is_deleted=False
    ).prefetch_related('images')

    activity_logs = ActivityLog.objects.filter(
        user=request.user
    ).order_by('-timestamp')[:10]

    context = {
        'available_posts': available_posts.count(),
        'claimed_posts': claimed_posts,
        'activity_logs': activity_logs,
    }

    return render(request, 'user/dashboard.html', context)


@login_required
def verification_pending(request):
    if request.user.status == 'verified':
        return redirect('accounts:user_dashboard')

    if request.user.role == 'manager':
        return redirect('accounts:manager_dashboard')

    return render(request, 'user/pending_verification.html')


@login_required
def user_posts(request):
    if not is_verified(request.user):
        return redirect('accounts:verification_pending')

    claimed_posts = Post.objects.filter(
        claimed_by=request.user,
        is_deleted=False
    ).prefetch_related('images').order_by('-created_at')

    return render(request, 'user/my_posts.html', {'claimed_posts': claimed_posts})


@login_required
def user_activity(request):
    activity_logs = ActivityLog.objects.filter(
        user=request.user
    ).order_by('-timestamp')

    return render(request, 'user/activity.html', {'activity_logs': activity_logs})


@login_required
@user_passes_test(is_manager)
def manager_dashboard(request):
    total_users = User.objects.count()
    verified_users = User.objects.filter(status='verified').count()
    pending_users = User.objects.filter(status='pending').count()
    blocked_users = User.objects.filter(status='blocked').count()

    total_posts = Post.objects.filter(is_deleted=False).count()
    available_posts = Post.objects.filter(status='available', is_deleted=False).count()
    claimed_posts = Post.objects.filter(status='claimed', is_deleted=False).count()
    completed_posts = Post.objects.filter(status='completed', is_deleted=False).count()
    approved_posts = Post.objects.filter(status='approved', is_deleted=False).count()

    online_users = User.objects.filter(is_online=True).count()

    recent_activity = ActivityLog.objects.select_related('user').order_by('-timestamp')[:20]
    all_posts = Post.objects.filter(is_deleted=False).order_by('-created_at')

    context = {
        'total_users': total_users,
        'verified_users': verified_users,
        'pending_users': pending_users,
        'blocked_users': blocked_users,
        'total_posts': total_posts,
        'available_posts': available_posts,
        'claimed_posts': claimed_posts,
        'completed_posts': completed_posts,
        'approved_posts': approved_posts,
        'online_users': online_users,
        'recent_activity': recent_activity,
         'all_posts': all_posts,
    }

    return render(request, 'manager/dashboard.html', context)


@login_required
@user_passes_test(is_manager)
def manage_users(request):
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')

    users = User.objects.all().order_by('-created_at')

    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )

    if status_filter:
        users = users.filter(status=status_filter)

    context = {
        'users': users,
        'search_query': search_query,
        'status_filter': status_filter,
    }

    return render(request, 'manager/manage_users.html', context)


@login_required
@user_passes_test(is_manager)
@require_http_methods(["POST"])
def verify_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.status = 'verified'
    user.save()

    ActivityLog.objects.create(
        user=request.user,
        action='verify',
        details=f"Verified user {user.username}",
        ip_address=get_client_ip(request),
    )

    messages.success(request, f'{user.username} has been verified!')
    return redirect('accounts:manage_users')


@login_required
@user_passes_test(is_manager)
@require_http_methods(["POST"])
def reject_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.status = 'rejected'
    user.save()

    ActivityLog.objects.create(
        user=request.user,
        action='reject',
        details=f"Rejected user {user.username}",
        ip_address=get_client_ip(request),
    )

    messages.success(request, f'{user.username} has been rejected!')
    return redirect('accounts:manage_users')


@login_required
@user_passes_test(is_manager)
@require_http_methods(["POST"])
def block_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.status = 'blocked'
    user.is_active = False
    user.save()

    ActivityLog.objects.create(
        user=request.user,
        action='block',
        details=f"Blocked user {user.username}",
        ip_address=get_client_ip(request),
    )

    messages.success(request, f'{user.username} has been blocked!')
    return redirect('accounts:manage_users')


@login_required
@user_passes_test(is_manager)
def activity_logs(request):
    logs = ActivityLog.objects.select_related('user').order_by('-timestamp')

    action_filter = request.GET.get('action', '')
    if action_filter:
        logs = logs.filter(action=action_filter)

    context = {
        'logs': logs,
        'action_filter': action_filter,
    }

    return render(request, 'manager/activity_logs.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserManagementForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserManagementForm(instance=request.user)

    return render(request, 'user/profile.html', {'form': form})

