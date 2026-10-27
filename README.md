# 🏨 RoomReserve API

A production-ready REST API for room reservation management, built with Django REST Framework.
**🔗 Live Demo:** [https://roomreseration-g9ex.onrender.com/api/docs/](https://roomservation-g9ex.onrender.com/api/docs/)

---
## ✨ Key Features
- **JWT Authentication**: Secure login with access & refresh tokens.
- **Business Logic**: Prevents overlapping reservations. Simulates payment (pending -> confirmed).
- **Custom Actions**: Cancel own reservations, pay for pending reservations.
- **Advanced DRF**: Pagination (`?page=2`), Filtering(`?room=1 or capacity=5`), Search(`?search=paris`), Ordering(`?ordering=-capacity, ordering=-start_time`).
- **Auto-Documentation**: Interactive Swagger UI generated with `drf-spectacular`.
- **Fully Tested**: 13 automated tests covering models, views, auth, and edge cases.
- **Dockerized**: Ready to run anywhere with Docker Compose.

---
## 🛠️ Tech Stack 
- **Backend**: Python 3.13, Django 6, Django REST Framework
- **Database**: PostgreSQL (Production), SQLite (Tests)
- **Auth**: JWT (`djangorestframework-simplejwt`)
- **Documentation**: Swagger (`drf-spectacular`)
- **Infrastructure**: Docker, Render, Gunicorn
- **Testing**: pytest, pytest-django

---

## 🚀 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/token/` | Login (returns JWT access & refresh) |
| `POST` | `/api/token/refresh/` | Refresh access token |
| `POST` | `/api/rooms/v2/` | Create a room |
| ` GET` | `/api/rooms/v2/`| List rooms (paginated, searchable) |
| `GET` | `/api/rooms/v2/{id}/` | Get room details |
| `PATCH` | `/api/rooms/v2/{id}/` | Update a room |
| `DELETE` | `/api/rooms/v2/{id}/` | Delete a room |

| `Get` | `/api/rooms/stats/` | Top 5 most booked rooms |

| `POST` | `/api/reservations/v2/` | Create a reservation (auto-attaches user) |
| `GET` | `/api/reservations/v2/` | List reservations |
| `GET` | `/api/reservations/v2/` | List reservations |
| `POST` | `/api/reservations/v2/{id}/pay/` | Simulate payment (confirms reservation) |
| `POST` | `/api/reservations/v2/{id}/cancel/` | Cancel reservation |
| `GET` | `/api/docs/` | Swagger UI Documentation |

#🐳 Run Locally
```bash
# 1. Clone the reposity
git clone https://github.com/Mahamat-sultan-mahamat01/roomreserve.git
cd roomreserve
# 2. Start containers
docker compose up --build -d

# 3. Run migrations
docker compose exec web python manage.py migrate
# 4? Create a superuser
docker compose exec web python manage.py createsuperuser

# 5. Access the API
# Swagger: http://localhost:8000/api/docs/
# Admin: http://localhost:8000/admin/
---
##  🧪 Testing
The project includes a full suite of automated tests:
```bash
python -m pytest -s -v
