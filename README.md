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

## Test UI

The `test_ui/` directory contains simple HTML pages for interacting with the
API without a frontend framework. Open the files directly in your browser and
ensure the backend is running.

- `signup.html` – create a new account.
- `login.html` – obtain an API token which is stored in `localStorage`.
- `create-car.html` – create a car listing (requires login).
- `my-cars.html` – view your car listings.
