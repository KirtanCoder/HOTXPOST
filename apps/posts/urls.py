from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.posts_list, name='list'),
    path('<int:post_id>/', views.post_detail, name='detail'),
    path('create/', views.create_post, name='create'),
    path('<int:post_id>/edit/', views.edit_post, name='edit'),
    path('<int:post_id>/delete/', views.delete_post, name='delete'),
    path('<int:post_id>/claim/', views.claim_post, name='claim'),
    path('<int:post_id>/complete/', views.mark_completed, name='complete'),
    path('<int:post_id>/approve/', views.approve_post, name='approve'),
    path('image/<int:image_id>/delete/', views.delete_image, name='delete_image'),
]
