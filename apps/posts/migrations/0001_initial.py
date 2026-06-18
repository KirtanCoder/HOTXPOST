# Generated initial migration for posts

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('community', models.CharField(max_length=255)),
                ('twitter_link', models.URLField(max_length=500)),
                ('comment_text', models.TextField()),
                ('hashtags', models.TextField(help_text='Comma-separated hashtags')),
                ('status', models.CharField(choices=[('available', 'Available'), ('claimed', 'Claimed'), ('completed', 'Completed'), ('approved', 'Approved')], default='available', max_length=20)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('claimed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='claimed_posts', to='accounts.user')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_posts', to='accounts.user')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField()),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='posts.post')),
            ],
            options={
                'ordering': ['uploaded_at'],
            },
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['status'], name='posts_post_status_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['claimed_by'], name='posts_post_claimed__idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['is_deleted'], name='posts_post_is_dele_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['-created_at'], name='posts_post_created_idx'),
        ),
    ]
