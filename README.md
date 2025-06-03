# DjangoGramm - Mini Instagram Clone with Django 🚀

**DjangoGramm** is a mini Instagram-like application where users can register, publish posts, like them, follow other users, and edit their profile.

---

## 📌 Main Features

✅ **User registration with email confirmation** (via email link)  
✅ **User authentication** (login/logout)  
✅ **User profile page** (name, email, avatar, bio, followers)  
✅ **Create and display image posts**  
✅ **Tag system** (search by tags, add new tags)  
✅ **Like system** (like and unlike posts)  
✅ **Post feed** (sorted by date)  
✅ **User subscriptions** (follow/unfollow)  
✅ **Webpack and SCSS integration**  

---

## 👆 Installation & Setup

### 1️⃣ Clone the repository
```
git clone git@git.foxminded.ua:foxstudent107439/task_15.git
cd 15
```

### 2️⃣  Create and activate virtual environment
```
python -m venv venv
source venv/bin/activate  # MacOS/Linux
venv\Scripts\activate     # Windows
```

### 3️⃣ Install dependencies

```
pip install -r requirements.txt
npm install
```

### 4️⃣ Configure environment variables (.env)
Create a .env file and add the following:
```
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgres://user:password@localhost:5432/djangogramm
```

### 5️⃣ Apply migrations
```
python manage.py migrate
```

### 6️⃣ Create superuser
```
python manage.py createsuperuser
```

### 7️⃣ Build frontend (Webpack)
```
npx webpack --mode production
```

### 8️⃣ Run the development server
```
python manage.py runserver
```

App will be available at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🔒 Authentication

### 📌 Регистрация пользователя
📌 User Registration
Go to http://127.0.0.1:8000/users/register/
Fill out the form and provide your email
Confirm your email via the received link
Log in after confirmation

### Login
Visit http://127.0.0.1:8000/users/login/
Enter credentials to log in

### 📌 Logout
Visit http://127.0.0.1:8000/users/logout/
You will be redirected to the login page

---

## 🛠 Technologies Used

- **Backend:** Django 5.1.5, Django REST Framework
- **Database:** PostgreSQL (in prod)
- **Frontend:** JavaScript, Webpack, SCSS, Bootstrap
- **Forms & Validation:** Django Forms
- **Messages & Notifications:** Django Messages
- **Debugging:** Django Debug Toolbar

---

## 👤Subscriptions & Likes

- **Subscriptions:** You can subscribe to other users.
- **Subscriptions display:** "Subscribe" or "Unsubscribe" button.
- **Likes:** Put and remove likes under posts.
---

## 📂 Project structure

```
django_gramm/                  # Root directory of the Django project
├── django_gramm/              # Main Django project folder (configuration)
│   ├── __init__.py            # Package initialization file
│   ├── asgi.py                # ASGI server configuration
│   ├── settings.py            # Main settings file for the Django project
│   ├── urls.py                # Root URL configuration
│   ├── wsgi.py                # WSGI server configuration
│
├── frontend/                  # Frontend source files
│   ├── dist/                  # Compiled assets (via Webpack)
│   │   ├── bundle.js          # Main compiled JavaScript file
│   │   ├── bundle.js.LICENSE.txt  # Webpack license info
│   ├── src/                   # Raw frontend source code
│   │   ├── index.js           # Webpack entry point
│   │   ├── main.js            # Main JavaScript logic
│   │   ├── styles.scss        # Main SCSS styles
│
├── media/                     # User-uploaded media files
│   ├── avatars/               # Folder for user profile pictures
│   │   ├── IMG_0354_Original.jpeg  # Example uploaded image
│   │   ├── IMG_8105.jpeg      # Another uploaded image
│   │   ├── IMG_20190707_194001_815_Original.jpeg  # Another sample image
│
├── node_modules/              # npm packages (installed via `npm install`)
│
├── posts/                     # App for managing posts
│   ├── migrations/            # Django database migrations
│   ├── static/                # Static files (not used directly)
│   ├── templates/posts/       # HTML templates for posts
│   │   ├── create_post.html   # Template for creating a post
│   │   ├── post_detail.html   # Template for post detail view
│   │   ├── post_list.html     # Template for post list
│   ├── tests/                 # Tests for the `posts` app
│   ├── __init__.py            # Package initialization
│   ├── admin.py               # Admin configuration for posts
│   ├── apps.py                # App configuration for `posts`
│   ├── forms.py               # Forms for creating/editing posts
│   ├── models.py              # Post database models
│   ├── views.py               # View logic for posts
│   ├── urls.py                # URL routing for `posts` app
│
├── static/                    # Project-wide static files
│   ├── css/                   # CSS files
│   ├── frontend/              # Compiled frontend files
│   │   ├── bundle.js          # Compiled frontend JS
│   │   ├── bundle.js.LICENSE.txt  # Webpack license file
│   ├── js/                    # JavaScript files
│   ├── favicon.ico            # Website favicon
│
├── staticfiles/               # Collected static files (`collectstatic` output)
│   ├── admin/                 # Django admin static files
│   ├── cloudinary/            # Cloudinary-related files (if used)
│   ├── css/                   # Collected CSS files
│   ├── debug_toolbar/         # Django Debug Toolbar static files
│   ├── frontend/              # Collected frontend files
│   ├── js/                    # Collected JavaScript files
│
├── templates/                 # Project-wide HTML templates
│   ├── base.html              # Base HTML layout
│   ├── home.html              # Homepage template
│
├── users/                     # App for user management
│   ├── migrations/            # Database migrations for users
│   ├── templates/users/       # HTML templates for user-related pages
│   │   ├── edit_profile.html  # Profile edit page
│   │   ├── email_already_confirmed.html  # Email already confirmed message
│   │   ├── login.html         # Login page
│   │   ├── profile.html       # User profile page
│   │   ├── register.html      # Registration page
│   │   ├── registration_pending.html  # Waiting for email confirmation
│   ├── tests/                 # Tests for the `users` app
│   ├── __init__.py            # Package initialization
│   ├── admin.py               # Admin configuration for users
│   ├── apps.py                # App configuration for `users`
│   ├── forms.py               # Forms for user creation and editing
│   ├── models.py              # User database models
│   ├── views.py               # View logic for users
│   ├── urls.py                # URL routing for `users` app
│
├── tests/                     # General project-level tests
│   ├── __init__.py            # Package initialization
│   ├── test_forms.py          # Tests for forms
│   ├── test_models.py         # Tests for models
│   ├── test_views.py          # Tests for views
│
├── .env                       # Environment variables file (do not commit)
├── .gitignore                 # Git ignore rules
├── debug.log                  # Log file (ignored by Git)
├── manage.py                  # Django management utility
├── package.json               # npm package configuration
├── package-lock.json          # Auto-generated npm dependency lock file
├── pytest.ini                 # Pytest configuration
├── README.md                  # Project documentation
├── requirements.txt           # Python dependencies
├── webpack.config.js          # Webpack configuration file


---

## 🚀 Deployment
Configure .env file on the server
Run docker-compose up -d
Apply migrations: python manage.py migrate
Collect static files: python manage.py collectstatic
Start Gunicorn or Uvicorn (if using ASGI)
---

## 👨‍💻 Author

🌟 Developer: Ivan Revchuk
🌟 Mentor: Foxminded Team

---
📜 License
This project is licensed under the MIT License. See the LICENSE file for more info.
