# Deployment Guide - Twitter Task Manager

## Deploying to Render.com

Render is the recommended platform for deploying this Django application. It's free to start and handles all the complexity of deployment.

### Prerequisites

- GitHub account with the project repository
- Render account (https://render.com)
- Cloudinary account with API credentials
- Domain name (optional)

### Step 1: Prepare Your Repository

1. Make sure your code is committed and pushed to GitHub:
```bash
git add .
git commit -m "Initial commit: Twitter Task Manager"
git push origin main
```

2. Ensure `.env.local` is in `.gitignore` to avoid pushing secrets

### Step 2: Create Render Web Service

1. Go to https://render.com and sign in
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Select the branch you want to deploy (main)
5. Fill in the service details:
   - **Name**: twitter-task-manager
   - **Runtime**: Python 3.11
   - **Build Command**: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn twitter_task_manager.wsgi:application`

### Step 3: Add Environment Variables

In the Render dashboard, go to "Environment" and add:

```
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-app.onrender.com,yourdomain.com
DATABASE_URL=postgresql://...
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### Step 4: Generate SECRET_KEY

Locally, generate a secure SECRET_KEY:

```bash
python manage.py shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
# Copy the output and paste in Render environment
```

### Step 5: Database Setup

#### Option A: Use Render PostgreSQL (Recommended)

1. In Render dashboard, create a "PostgreSQL" database
2. Copy the database URL
3. Add to environment variable: `DATABASE_URL=<copied-url>`

#### Option B: Continue with SQLite

For small projects, SQLite works fine:
```
DATABASE_URL=sqlite:///db.sqlite3
```

### Step 6: Create Superuser

After the first deployment:

1. Go to your deployed app URL
2. In Render, open the Shell
3. Run:
```bash
python manage.py createsuperuser
```

### Step 7: Deploy

Click "Deploy" in Render. The build process will:
1. Install dependencies
2. Run migrations
3. Collect static files
4. Start the server

### Step 8: Verify Deployment

1. Visit your app URL
2. Test signup, login, and basic functionality
3. Go to `/admin/` and log in with superuser credentials

## Deploying to Railway.app

Alternative to Render:

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub"
4. Select your repository
5. Add PostgreSQL database
6. Set environment variables
7. Deploy

## Deploying to PythonAnywhere

For a simpler approach:

1. Sign up at https://www.pythonanywhere.com
2. Upload files via their web interface
3. Create a virtual environment
4. Install dependencies
5. Configure Web App
6. Set environment variables
7. Reload

## Post-Deployment Checklist

- [ ] Set `DEBUG=False`
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Set `SECURE_SSL_REDIRECT=True` in settings
- [ ] Set `SESSION_COOKIE_SECURE=True`
- [ ] Set `CSRF_COOKIE_SECURE=True`
- [ ] Configure custom domain (if applicable)
- [ ] Set up SSL certificate
- [ ] Test all features
- [ ] Monitor error logs
- [ ] Set up automated backups

## Scaling Considerations

### Database
- Start with PostgreSQL free tier on Render
- Upgrade when you need more resources
- Enable automated backups

### Storage
- Use Cloudinary for all media files
- Never store images on the server
- Set reasonable file size limits

### Performance
- Enable Django caching
- Use database query optimization
- Monitor server logs
- Set up error tracking (Sentry)

## Monitoring & Maintenance

### Logs
View logs in Render dashboard:
- Application logs
- Build logs
- Deploy logs

### Health Checks
Render automatically monitors:
- Response time
- Error rates
- CPU usage
- Memory usage

### Updates
Keep dependencies updated:
```bash
pip list --outdated
pip install --upgrade package-name
```

## Troubleshooting

### Build Fails
- Check build logs in Render
- Verify all dependencies in requirements.txt
- Ensure migrations are correct

### Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
```

### Database Connection Error
- Verify DATABASE_URL environment variable
- Check database is running
- Test connection locally first

### Cloudinary Issues
- Verify API credentials are correct
- Check environment variables are set
- Test upload locally first

### 500 Error
- Check logs in Render dashboard
- Look for database connection issues
- Verify environment variables

## Security Best Practices

1. **Never commit .env files**
   - Use .env.example as template
   - Always use Render's environment variables

2. **Change SECRET_KEY regularly**
   - Generate new key for production
   - Different keys for dev/production

3. **Use HTTPS only**
   - Enable in Render (automatic)
   - Redirect HTTP to HTTPS

4. **Backup database regularly**
   - Render provides automated backups
   - Export data periodically

5. **Monitor for suspicious activity**
   - Check admin logs
   - Set up error tracking
   - Monitor API usage

## Cost Estimation

### Render Free Tier
- Web Service: Free (spins down after 15 min inactivity)
- PostgreSQL: Free (100MB)
- Static Assets: Via Render CDN

### Paid Plans
- Web Service: $7/month (always on)
- PostgreSQL: $7/month (1GB)
- PostgreSQL: $35/month (10GB)

### Cloudinary Free Tier
- 25 credits/month
- Unlimited storage for free images
- Good for small to medium projects

## Upgrading from Free to Paid

1. In Render, click on Web Service
2. Scroll to "Plan"
3. Click "Upgrade"
4. Choose Standard plan ($7/month)
5. Billing starts immediately

## Custom Domain

1. In Render, go to "Settings"
2. Add Custom Domain
3. Update DNS records at your registrar
4. Wait for DNS propagation (24-48 hours)

## SSL Certificate

Render automatically provides:
- Free SSL certificate
- Auto-renewal
- HTTPS for custom domains

## API Monitoring

Set up error tracking with Sentry:
```bash
pip install sentry-sdk
```

Add to settings.py:
```python
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0
)
```

## Performance Optimization for Production

1. Enable Django caching
2. Use CDN for static files
3. Optimize database queries
4. Implement rate limiting
5. Use pagination for large datasets
6. Compress responses with gzip

## Backup & Recovery

### Backup Database
```bash
# Via Render shell
pg_dump $DATABASE_URL > backup.sql
```

### Restore Database
```bash
# Via Render shell
psql $DATABASE_URL < backup.sql
```

## Next Steps

1. Deploy to Render
2. Create admin account
3. Verify all features work
4. Add custom domain
5. Set up monitoring
6. Celebrate! 🎉

For more help, visit:
- Render Docs: https://docs.render.com
- Django Docs: https://docs.djangoproject.com
- Cloudinary Docs: https://cloudinary.com/documentation
