# Quick Start Guide - Twitter Task Manager

Get up and running in 5 minutes!

## Windows Users

### Step 1: Run Setup
```bash
setup.bat
```

This will:
- Create virtual environment
- Install dependencies
- Create database
- Create superuser

### Step 2: Edit Configuration
Open `.env` and add your Cloudinary credentials:
```
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### Step 3: Start Server
```bash
venv\Scripts\activate
python manage.py runserver
```

Visit: http://localhost:8000

---

## macOS/Linux Users

### Step 1: Run Setup
```bash
chmod +x setup.sh
./setup.sh
```

### Step 2: Edit Configuration
```bash
nano .env
```

Add Cloudinary credentials

### Step 3: Start Server
```bash
source venv/bin/activate
python manage.py runserver
```

---

## First Time User Workflow

### 1. Admin Setup
- Go to: http://localhost:8000/admin/
- Login with superuser credentials

### 2. Create a Post
- Click "Add Post"
- Fill in details:
  - Title: "Tweet about new feature"
  - Community: "Tech Twitter"
  - Twitter Link: "https://twitter.com/..."
  - Comment: "Amazing new update!"
  - Hashtags: "#tech, #update, #awesome"
  - Upload images (optional)
- Save

### 3. Create a Test User
- Go to: http://localhost:8000/accounts/signup/
- Fill in:
  - Name: John Doe
  - Username: johndoe
  - Email: john@example.com
  - Discord: johndoe#1234
  - Password: SecurePassword123
- Submit

### 4. Verify User
- Go back to admin panel
- Find the user under "Users"
- Change status to "Verified"
- Save

### 5. Test User Flow
- Logout from admin
- Go to: http://localhost:8000/accounts/login/
- Login as the new user
- View available posts
- Claim a post
- Copy comment text
- Open Twitter link
- Mark as completed

### 6. Manager Approval
- Go to admin and change post status to "Approved"

---

## Project Structure at a Glance

```
/c/Users/kirta/Desktop/marketting/
├── manage.py ← Run commands here
├── requirements.txt ← Dependencies
├── .env ← Your secrets (create from .env.example)
├── twitter_task_manager/ ← Project settings
│   ├── settings.py ← Main configuration
│   ├── urls.py ← URL routing
│   ├── wsgi.py ← WSGI config
│   └── middleware.py ← User online tracking
├── apps/
│   ├── accounts/ ← User management
│   └── posts/ ← Post management
├── templates/ ← HTML files
├── static/ ← CSS, JavaScript
├── db.sqlite3 ← Database (created by migrate)
└── logs/ ← Application logs
```

---

## Common Commands

```bash
# Start server
python manage.py runserver

# Create migrations (after changing models)
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Access Django shell
python manage.py shell

# Reset database (development only)
rm db.sqlite3
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Run tests
python manage.py test
```

---

## Cloudinary Setup (5 mins)

1. Go to: https://cloudinary.com/users/register/free
2. Sign up with email
3. Verify email
4. Go to Dashboard
5. Copy:
   - Cloud Name
   - API Key
   - API Secret
6. Paste into `.env` file

---

## User Types & Access

### Regular User
- Sign up
- Wait for manager verification
- View available posts
- Claim posts
- Copy comment/hashtags
- Mark posts as completed
- View activity log

### Manager
- Login with admin credentials
- Create/edit/delete posts
- Verify/reject/block users
- View system dashboard
- Monitor activity logs
- Approve completed posts

---

## Features Overview

### Posts
- Create with title, description, images
- Multi-image upload to Cloudinary
- Status: Available → Claimed → Completed → Approved
- Soft delete (posts never permanently removed)
- Search and filter

### Users
- Email-based authentication
- Discord username support
- Verification system
- Online tracking
- Activity logging
- Role-based access

### Dashboard
- Stats overview
- Recent activity
- Quick actions
- User management
- Post management

---

## Troubleshooting

### Port 8000 already in use
```bash
python manage.py runserver 8001
```

### Database errors
```bash
python manage.py migrate
```

### Static files not loading
```bash
python manage.py collectstatic --clear --noinput
```

### Cloudinary not working
- Check .env file has correct values
- Verify no typos in credentials
- Test in Django admin

### Can't login
- Check user status is "verified"
- Verify email is correct
- Reset password if needed

---

## Next Steps

1. ✓ Complete setup
2. ✓ Create posts
3. ✓ Create test users
4. ✓ Test the workflow
5. → Deploy to Render (see DEPLOYMENT.md)
6. → Add your domain
7. → Go live!

---

## Getting Help

### Documentation
- README.md - Full documentation
- DEPLOYMENT.md - Deployment guide
- Django Docs: https://docs.djangoproject.com

### Common Issues
Check the README.md "Troubleshooting" section

### Code Issues
Check django.log in the logs/ folder

---

**Enjoy using Twitter Task Manager!** 🚀

Questions? Check the docs or create an issue on GitHub.
