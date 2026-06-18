# Twitter Task Manager - Django Application

A complete production-ready Django web application for managing Twitter/X engagement tasks with user verification, post management, and activity tracking.

## Features

### User Management
- User registration and authentication
- Email-based login
- User roles (User & Manager)
- User status tracking (pending, verified, rejected, blocked)
- Online user tracking
- Activity logging

### Post Management
- Create, edit, delete posts
- Multiple image uploads via Cloudinary
- Post claiming system
- Task completion workflow
- Post approval system
- Soft delete functionality

### Dashboard Features
- User dashboard with task overview
- Manager dashboard with system statistics
- Activity history tracking
- Real-time online user status

### Authentication & Security
- Django's built-in authentication
- Password hashing
- Session-based authentication
- CSRF protection
- SQL injection prevention
- User role-based access control

## Project Structure

```
twitter_task_manager/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── db.sqlite3
├── twitter_task_manager/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   ├── middleware.py
│   └── context_processors.py
├── apps/
│   ├── accounts/
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   ├── admin.py
│   │   └── apps.py
│   └── posts/
│       ├── migrations/
│       ├── models.py
│       ├── views.py
│       ├── urls.py
│       ├── forms.py
│       ├── admin.py
│       └── apps.py
├── templates/
│   ├── base.html
│   ├── auth/
│   ├── user/
│   ├── manager/
│   └── posts/
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── logs/
```

## Installation & Setup

### 1. Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### 2. Clone the Repository
```bash
cd /c/Users/kirta/Desktop/marketting
```

### 3. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Environment Configuration
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual values
# Get Cloudinary credentials from https://cloudinary.com
```

### 6. Database Migration
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### 7. Create Superuser
```bash
python manage.py createsuperuser
```

### 8. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 9. Run Development Server
```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

## Database Models

### User Model
- Custom user model with email as primary identifier
- Fields: username, email, first_name, last_name, discord_username, role, status, is_online, last_seen

### Post Model
- title, community, twitter_link, comment_text, hashtags
- Status: available, claimed, completed, approved
- Support for multiple images via PostImage model

### PostImage Model
- Stores Cloudinary image URLs
- Links to Post model

### ActivityLog Model
- Tracks all user and system actions
- Stores user, action type, details, timestamp, IP address

## API Endpoints

### Authentication
- `GET/POST /accounts/signup/` - User registration
- `GET/POST /accounts/login/` - User login
- `POST /accounts/logout/` - User logout

### User Dashboard
- `GET /accounts/user/dashboard/` - User dashboard
- `GET /accounts/user/verification-pending/` - Pending verification
- `GET /accounts/user/posts/` - My claimed posts
- `GET /accounts/user/activity/` - User activity log
- `GET/POST /accounts/user/profile/` - User profile

### Posts
- `GET /posts/` - List available posts
- `GET /posts/<id>/` - Post detail
- `POST /posts/<id>/claim/` - Claim a post
- `POST /posts/<id>/complete/` - Mark post completed

### Manager Routes
- `GET /accounts/manager/dashboard/` - Manager dashboard
- `GET /accounts/manager/users/` - Manage users
- `POST /accounts/manager/users/<id>/verify/` - Verify user
- `POST /accounts/manager/users/<id>/reject/` - Reject user
- `POST /accounts/manager/users/<id>/block/` - Block user
- `GET/POST /posts/create/` - Create post
- `GET/POST /posts/<id>/edit/` - Edit post
- `POST /posts/<id>/delete/` - Delete post
- `POST /posts/<id>/approve/` - Approve completed post

## Cloudinary Configuration

1. Sign up at [Cloudinary](https://cloudinary.com)
2. Get your credentials:
   - Cloud Name
   - API Key
   - API Secret
3. Add to .env file:
```
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

## User Workflow

### For Regular Users
1. Sign up with email, username, name
2. Wait for manager verification
3. Once verified, view available posts
4. Claim a post
5. Copy comment text and hashtags
6. Open Twitter link in new tab
7. Post the comment with hashtags
8. Mark post as completed in dashboard
9. Wait for manager approval

### For Managers
1. Log in with admin credentials
2. View system dashboard with statistics
3. Create new posts with images
4. Verify, reject, or block users
5. View activity logs
6. Approve completed tasks

## Security Features

- Password hashing with Django's built-in system
- CSRF protection on all forms
- SQL injection prevention via ORM
- XSS protection with template escaping
- Session-based authentication
- Secure password validators
- User role-based access control
- Activity logging for audit trail

## Responsive Design

- Mobile-first approach
- Tablet and desktop optimization
- Touch-friendly interface
- Dark mode support (system preference)
- Modern CSS Grid and Flexbox
- Smooth animations and transitions

## Deployment

### For Render.com

1. Create account on [Render](https://render.com)
2. Connect your GitHub repository
3. Create Web Service:
   - Build command: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - Start command: `gunicorn twitter_task_manager.wsgi:application`
4. Add Environment Variables:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=False
   ALLOWED_HOSTS=your-domain.onrender.com
   DATABASE_URL=your-database-url
   CLOUDINARY_CLOUD_NAME=your_cloud_name
   CLOUDINARY_API_KEY=your_api_key
   CLOUDINARY_API_SECRET=your_api_secret
   ```

### For Production

1. Update settings.py:
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   SECURE_SSL_REDIRECT = True
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True
   ```

2. Generate new SECRET_KEY:
   ```bash
   python manage.py shell
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   ```

3. Use PostgreSQL instead of SQLite
4. Set up proper logging
5. Enable HTTPS
6. Use environment variables for secrets

## Admin Panel

Access Django admin at `/admin/`

Features:
- Manage users and their status
- View and manage posts
- Monitor activity logs
- Create custom admin filters

## Troubleshooting

### Database Issues
```bash
# Reset database (development only)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Static Files
```bash
# If static files not loading
python manage.py collectstatic --clear --noinput
```

### Image Upload Issues
- Verify Cloudinary credentials
- Check file size (max 5MB recommended)
- Ensure image format is supported

### Authentication Issues
- Clear browser cookies
- Check user status in admin panel
- Verify email is correct

## Technologies Used

- **Backend**: Django 4.2
- **Database**: SQLite (development), PostgreSQL (production)
- **Image Storage**: Cloudinary
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Authentication**: Django Auth
- **Deployment**: Render, Netlify, Vercel (backend on Render)

## Performance Optimization

- Database query optimization with `select_related()` and `prefetch_related()`
- CSS minification in production
- JavaScript debouncing for search
- Image lazy loading
- Database indexing on frequently queried fields
- Browser caching headers

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers

## License

MIT License

## Support

For issues and questions, please create an issue on GitHub or contact the development team.

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## Future Enhancements

- Real-time notifications with WebSockets
- Email notifications
- Advanced analytics and reporting
- Two-factor authentication
- API key management for developers
- Bulk post operations
- Post scheduling
- Template system for posts
- Team collaboration features
- Custom branding options

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Maintainer**: Your Name
