from apps.accounts.models import User
from apps.posts.models import Post

def user_context(request):
    context = {
        'is_manager': False,
        'total_posts': 0,
        'available_posts': 0,
        'claimed_posts': 0,
        'completed_posts': 0,
    }

    if request.user.is_authenticated:
        context['is_manager'] = request.user.role == 'manager'

        if context['is_manager']:
            context['total_posts'] = Post.objects.filter(is_deleted=False).count()
            context['available_posts'] = Post.objects.filter(status='available', is_deleted=False).count()
            context['claimed_posts'] = Post.objects.filter(status='claimed', is_deleted=False).count()
            context['completed_posts'] = Post.objects.filter(status='completed', is_deleted=False).count()
        else:
            context['available_posts'] = Post.objects.filter(status='available', is_deleted=False).count()
            context['claimed_posts'] = Post.objects.filter(claimed_by=request.user, status='claimed', is_deleted=False).count()
            context['completed_posts'] = Post.objects.filter(claimed_by=request.user, status='completed', is_deleted=False).count()

    return context
