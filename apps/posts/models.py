from django.db import models
from django.utils import timezone
from apps.accounts.models import User

class Post(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('claimed', 'Claimed'),
        ('completed', 'Completed'),
        ('approved', 'Approved'),
    )

    title = models.CharField(max_length=255)
    community = models.CharField(max_length=255)
    twitter_link = models.URLField(max_length=500)
    comment_text = models.TextField()
    hashtags = models.TextField(help_text="Comma-separated hashtags")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    claimed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='claimed_posts')

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_posts')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['claimed_by']),
            models.Index(fields=['is_deleted']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"

    def get_hashtags_list(self):
        return [tag.strip() for tag in self.hashtags.split(',') if tag.strip()]

    def is_claimable(self):
        return self.status == 'available' and not self.is_deleted

    def mark_completed(self):
        if self.status == 'claimed':
            self.status = 'completed'
            self.save()
            return True
        return False

    def mark_approved(self):
        if self.status == 'completed':
            self.status = 'approved'
            self.save()
            return True
        return False


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['uploaded_at']

    def __str__(self):
        return f"Image for {self.post.title}"
