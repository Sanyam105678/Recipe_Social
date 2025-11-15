# RecipeSocial Backend (Django + DRF)

A Social Media Platform backend focused on **sharing and rating recipes**. Supports two types of users: **Customers** and **Sellers**.

* **Customers:** View recipes & rate them.
* **Sellers:** Add recipes with images, names, and descriptions.

Built with: **Django, Django REST Framework (DRF), Celery, Redis, Pillow, AWS S3**.

---

## Table of Contents

1. Project Setup
2. Database
3. Running the Server
4. APIs
5. Testing
6. Folder Structure
7. Flow Overview

---

## Project Setup

1. Clone the repository:

```bash
git clone <repo_url>
cd RecipeSocialBackend
```

2. Create virtual environment & activate:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create superuser (optional):

```bash
python manage.py createsuperuser
```



## Database

* Default: **SQLite** 
* Tables:

  * `core_recipe` → Stores recipes
  * `core_rating` → Stores ratings
  * Custom User model → Stores Customers & Sellers

---

## Running the Server

1. Start Django server:

```bash
python manage.py runserver
```

---

## APIs

### Auth APIs

| Endpoint              | Method | Description                        |
| --------------------- | ------ | ---------------------------------- |
| `/api/auth/register/` | POST   | Register a user (Customer/Seller)  |
| `/api/auth/login/`    | POST   | Obtain JWT access & refresh tokens |
| `/api/auth/refresh/`  | POST   | Refresh JWT access token           |

---

### Recipe APIs

| Endpoint             | Method    | Permissions   | Description                           |
| -------------------- | --------- | ------------- | ------------------------------------- |
| `/api/recipes/`      | GET       | Authenticated | List all recipes                      |
| `/api/recipes/{id}/` | GET       | Authenticated | Get single recipe                     |
| `/api/recipes/`      | POST      | Seller only   | Add recipe (image, name, description) |
| `/api/recipes/{id}/` | PUT/PATCH | Seller only   | Update recipe (owner only)            |
| `/api/recipes/{id}/` | DELETE    | Seller only   | Delete recipe (owner only)            |

> **Note:** On creating a recipe, Celery compresses the image asynchronously.

---

### Rating APIs

| Endpoint             | Method    | Permissions | Description                                       |
| -------------------- | --------- | ----------- | ------------------------------------------------- |
| `/api/ratings/`      | GET       | Customer    | List ratings (filter by recipe using `?recipe=1`) |
| `/api/ratings/`      | POST      | Customer    | Add rating (1-5) to a recipe                      |
| `/api/ratings/{id}/` | PUT/PATCH | Customer    | Update rating (owner only)                        |
| `/api/ratings/{id}/` | DELETE    | Customer    | Delete rating (owner only)                        |

---

## Testing

1. Run Django server and ensure **Redis + Celery worker** running.
2. Test Auth APIs: Register & login both Customers & Sellers.
3. Test Recipe APIs:

   * Sellers can add/update/delete recipes
   * Customers can view recipes
4. Test Rating APIs:

   * Customers can rate recipes
   * `GET /api/ratings/?recipe=1` to view ratings

**Postman Tip:** Use query params in **Params tab** for GET requests (`?recipe=1`) instead of Body tab.

---

## Folder Structure

```
RecipeSocialBackend/
│
├─ recipesocial/          # Django project folder
│   ├─ __init__.py
│   ├─ settings.py
│   ├─ urls.py
│   ├─ celery.py
│   └─ wsgi.py
│
├─ core/                  # Main app
│   ├─ migrations/
│   ├─ tasks.py           # Celery tasks (image compress, emails, S3 backup)
│   ├─ models.py
│   ├─ serializers.py
│   ├─ views.py
│   ├─ urls.py
│   └─ permissions.py
│
├─ media/                 # Uploaded images
├─ manage.py
├─ requirements.txt
└─ README.md
```

---

## Commands Summary

| Action                   | Command                                               |
| ------------------------ | ----------------------------------------------------- |
| Activate venv            | `venv\Scripts\activate` or `source venv/bin/activate` |
| Install dependencies     | `pip install -r requirements.txt`                     |
| Make migrations          | `python manage.py makemigrations`                     |
| Apply migrations         | `python manage.py migrate`                            |
| Run server               | `python manage.py runserver`                          |
| Create superuser         | `python manage.py createsuperuser`                    |
| Test APIs                | Postman / Browser / curl                              |

---

## Flow Overview

1. **User registers → gets JWT token**
2. **Seller adds recipe → image compressed asynchronously by Celery**
3. **Customer views recipes → rates recipes**

Project is **fully functional** and static/media file handling.

```
```
