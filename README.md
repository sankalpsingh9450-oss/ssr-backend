# 🏗️ SSR Group Backend API

**FastAPI backend for [ssrgroupcivil.in](https://ssrgroupcivil.in)** — handles all form submissions, stores them in a database, and sends email notifications to the admin.

---

## Features

- **Contact Form** — General enquiries with subject categorization
- **Property Finder** — Property search requests with type, budget, and location
- **Material Enquiry** — Building material orders with quantity and delivery info
- **Partner Registration** — Business partner onboarding with category
- **Quote / BOQ Requests** — Free quotation and Bill of Quantities requests
- **Admin Dashboard** — View all submissions with pagination
- **Email Notifications** — Styled HTML emails sent on every submission
- **Auto API Docs** — Swagger UI at `/docs` and ReDoc at `/redoc`

---

## Tech Stack

| Layer       | Technology                     |
|-------------|--------------------------------|
| Framework   | FastAPI 0.115                  |
| Database    | SQLite (dev) / PostgreSQL (prod) |
| ORM         | SQLAlchemy 2.0 (async)         |
| Validation  | Pydantic v2                    |
| Email       | aiosmtplib (async SMTP)        |
| Server      | Uvicorn                        |

---

## Project Structure

```
ssr-backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py             # Settings via pydantic-settings
│   ├── database.py           # Async SQLAlchemy engine & session
│   ├── models/
│   │   ├── __init__.py
│   │   └── submissions.py    # All database models
│   ├── schemas/
│   │   └── __init__.py       # Pydantic request/response schemas
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── contact.py        # POST /api/v1/contact/
│   │   ├── property_finder.py# POST /api/v1/property-finder/
│   │   ├── materials.py      # POST /api/v1/materials/
│   │   ├── partners.py       # POST /api/v1/partners/
│   │   ├── quote.py          # POST /api/v1/quote/
│   │   └── admin.py          # GET  /api/v1/admin/...
│   └── services/
│       ├── __init__.py
│       └── email_service.py  # Email builder & sender
├── .env.example              # Environment template
├── requirements.txt
└── README.md
```

---

## Quick Start

### 1. Clone & Install

```bash
cd ssr-backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your actual values:

```env
SECRET_KEY=your-random-secret-key-here
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-gmail-app-password
ADMIN_EMAIL=info@ssrgroupcivil.in
```

> **Gmail App Password**: Go to Google Account → Security → 2-Step Verification → App Passwords → Generate one for "Mail".

### 3. Run the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The database tables are created automatically on first run.

### 4. Open API Docs

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## API Endpoints

All endpoints are prefixed with `/api/v1`.

### Form Submissions

| Method | Endpoint              | Description                |
|--------|-----------------------|----------------------------|
| POST   | `/contact/`           | Submit contact enquiry     |
| POST   | `/property-finder/`   | Submit property search     |
| POST   | `/materials/`         | Submit material enquiry    |
| POST   | `/partners/`          | Register as partner        |
| POST   | `/quote/`             | Request quotation or BOQ   |

### Admin (requires `?api_key=YOUR_SECRET_KEY`)

| Method | Endpoint                          | Description                  |
|--------|-----------------------------------|------------------------------|
| GET    | `/admin/dashboard`                | Summary counts of all forms  |
| GET    | `/admin/submissions/{form_type}`  | Paginated list of submissions|

**form_type** options: `contacts`, `property`, `materials`, `partners`, `quotes`

---

## Example API Calls

### Submit a Contact Form

```bash
curl -X POST http://localhost:8000/api/v1/contact/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Rahul Sharma",
    "email": "rahul@example.com",
    "phone": "+91-9876543210",
    "subject": "Construction Quote",
    "message": "I need a quote for building a 3BHK house in Greater Noida West."
  }'
```

### Submit a Property Finder Request

```bash
curl -X POST http://localhost:8000/api/v1/property-finder/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Priya Verma",
    "email": "priya@example.com",
    "phone": "+91-9123456789",
    "property_type": "Residential — Apartment",
    "budget_min": "40L",
    "budget_max": "70L",
    "preferred_location": "Noida Extension Sector 1-10",
    "requirements": "2BHK or 3BHK, gated society, near metro"
  }'
```

### View Admin Dashboard

```bash
curl "http://localhost:8000/api/v1/admin/dashboard?api_key=YOUR_SECRET_KEY"
```

### View Submissions (paginated)

```bash
curl "http://localhost:8000/api/v1/admin/submissions/contacts?api_key=YOUR_SECRET_KEY&page=1&per_page=10"
```

---

## Frontend Integration

Add these `fetch` calls to your frontend forms on ssrgroupcivil.in:

```javascript
// Example: Contact Form
const form = document.getElementById('contact-form');
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const response = await fetch('https://your-api-domain.com/api/v1/contact/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            name: form.name.value,
            email: form.email.value,
            phone: form.phone.value,
            subject: form.subject.value,
            message: form.message.value,
        }),
    });

    const result = await response.json();
    if (result.success) {
        alert(result.message);
        form.reset();
    }
});
```

---

## Production Deployment

### Option A: VPS (DigitalOcean, AWS EC2, etc.)

```bash
# Install dependencies
pip install -r requirements.txt gunicorn

# Run with Gunicorn + Uvicorn workers
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

Use **Nginx** as a reverse proxy in front of Gunicorn.

### Option B: Railway / Render (one-click deploy)

1. Push code to GitHub
2. Connect repo to Railway or Render
3. Set environment variables from `.env.example`
4. Deploy — it auto-detects Python + FastAPI

### Switch to PostgreSQL for Production

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/ssrgroup
```

Install the async driver:

```bash
pip install asyncpg
```

---

## Environment Variables

| Variable         | Required | Description                          |
|------------------|----------|--------------------------------------|
| `SECRET_KEY`     | Yes      | Used for admin API key auth          |
| `DATABASE_URL`   | No       | Defaults to SQLite                   |
| `CORS_ORIGINS`   | No       | Comma-separated allowed origins      |
| `SMTP_HOST`      | Yes*     | SMTP server hostname                 |
| `SMTP_PORT`      | Yes*     | SMTP port (587 for TLS)              |
| `SMTP_USER`      | Yes*     | SMTP username / email                |
| `SMTP_PASSWORD`  | Yes*     | SMTP password / app password         |
| `ADMIN_EMAIL`    | No       | Where notifications go               |

*Required for email notifications to work. The app runs fine without them — submissions are still saved to the database.

---

## License

Built for SSR Group Civil — [ssrgroupcivil.in](https://ssrgroupcivil.in)
