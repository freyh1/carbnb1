# Simple Django Auth Example

This project provides a minimal authentication backend using Django. The previous Next.js frontend has been removed in favour of basic HTML templates for login and signup.

## Installation

Ensure Docker and Docker Compose are installed. Copy `backend/.env.template` to `backend/.env` and adjust the values if needed.

### Local development

```bash
docker-compose up --build
```

Visit [http://localhost:8000/](http://localhost:8000/) to use the application.

### Admin Panel

To access the Django admin panel, create a superuser in the backend container:

```bash
docker exec -it backend bash
python manage.py createsuperuser
```

Then navigate to [http://localhost:8000/admin/](http://localhost:8000/admin/).
