from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import cloudinary
import cloudinary.uploader
from django.conf import settings

from .forms import PostForm
from .models import Post, PostImage
from apps.accounts.models import ActivityLog

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


@login_required
@user_passes_test(is_manager)
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.save()

            # Handle image uploads
            if 'images' in request.FILES:
                for image_file in request.FILES.getlist('images'):
                    try:
                        response = cloudinary.uploader.upload(image_file)
                        PostImage.objects.create(
                            post=post,
                            image_url=response['secure_url']
                        )
                    except Exception as e:
                        messages.warning(request, f"Failed to upload one image: {str(e)}")

            ActivityLog.objects.create(
                user=request.user,
                action='post_create',
                details=f"Created post '{post.title}'",
                ip_address=get_client_ip(request),
            )

            messages.success(request, 'Post created successfully!')
            return redirect('accounts:manager_dashboard')
    else:
        form = PostForm()

    return render(request, 'manager/create_post.html', {'form': form})


@login_required
@user_passes_test(is_manager)
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()

            # Handle new image uploads
            if 'images' in request.FILES:
                for image_file in request.FILES.getlist('images'):
                    try:
                        response = cloudinary.uploader.upload(image_file)
                        PostImage.objects.create(
                            post=post,
                            image_url=response['secure_url']
                        )
                    except Exception as e:
                        messages.warning(request, f"Failed to upload one image: {str(e)}")

            ActivityLog.objects.create(
                user=request.user,
                action='post_edit',
                details=f"Edited post '{post.title}'",
                ip_address=get_client_ip(request),
            )

            messages.success(request, 'Post updated successfully!')
            return redirect('accounts:manager_dashboard')
    else:
        form = PostForm(instance=post)

    context = {
        'form': form,
        'post': post,
        'images': post.images.all(),
    }

    return render(request, 'manager/edit_post.html', context)


@login_required
@user_passes_test(is_manager)
@require_http_methods(["POST"])
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.is_deleted = True
    post.save()

    ActivityLog.objects.create(
        user=request.user,
        action='post_delete',
        details=f"Deleted post '{post.title}'",
        ip_address=get_client_ip(request),
    )

    messages.success(request, 'Post deleted successfully!')
    return redirect('accounts:manager_dashboard')


@login_required
@user_passes_test(is_manager)
@require_http_methods(["POST"])
def delete_image(request, image_id):
    image = get_object_or_404(PostImage, id=image_id)
    post_id = image.post.id

    try:
        cloudinary.uploader.destroy(image.image_url.split('/')[-1].split('.')[0])
    except:
        pass

    image.delete()
    messages.success(request, 'Image deleted successfully!')
    return redirect('posts:edit', post_id=post_id)


@login_required
def posts_list(request):
    posts = Post.objects.filter(status='available', is_deleted=False).prefetch_related('images')
    return render(request, 'posts/list.html', {'posts': posts})


@login_required
@user_passes_test(is_verified)
@require_http_methods(["POST"])
def claim_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.status != 'available' or post.is_deleted:
        messages.error(request, 'This post is not available.')
        return redirect('accounts:user_dashboard')

    post.status = 'claimed'
    post.claimed_by = request.user
    post.save()

    ActivityLog.objects.create(
        user=request.user,
        action='post_claim',
        details=f"Claimed post '{post.title}'",
        ip_address=get_client_ip(request),
    )

    messages.success(request, 'Post claimed successfully!')
    return redirect('accounts:user_dashboard')


@login_required
@user_passes_test(is_verified)
@require_http_methods(["POST"])
def mark_completed(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.claimed_by != request.user or post.status != 'claimed':
        messages.error(request, 'You cannot complete this post.')
        return redirect('accounts:user_dashboard')

    post.status = 'completed'
    post.save()

    ActivityLog.objects.create(
        user=request.user,
        action='post_complete',
        details=f"Completed post '{post.title}'",
        ip_address=get_client_ip(request),
    )

    messages.success(request, 'Post marked as completed!')
    return redirect('accounts:my_posts')


@login_required
@user_passes_test(is_manager)
@require_http_methods(["POST"])
def approve_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.status != 'completed':
        messages.error(request, 'Only completed posts can be approved.')
        return redirect('accounts:manager_dashboard')

    post.status = 'approved'
    post.save()

    ActivityLog.objects.create(
        user=request.user,
        action='post_approve',
        details=f"Approved post '{post.title}' by {post.claimed_by.username}",
        ip_address=get_client_ip(request),
    )

    messages.success(request, 'Post approved successfully!')
    return redirect('accounts:manager_dashboard')


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.is_deleted and not (request.user.role == 'manager' or request.user == post.created_by):
        messages.error(request, 'This post has been deleted.')
        return redirect('accounts:user_dashboard')

    context = {
        'post': post,
        'images': post.images.all(),
        'can_claim': post.status == 'available' and request.user.status == 'verified' and not post.is_deleted,
        'can_complete': post.claimed_by == request.user and post.status == 'claimed',
        'can_approve': request.user.role == 'manager' and post.status == 'completed',
    }

    return render(request, 'posts/detail.html', context)
