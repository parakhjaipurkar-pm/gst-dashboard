# GST Dashboard

A Django REST API for tracking GST filing compliance across onboarded GSTINs.

## Features

- Models for onboarded GSTINs and their filing statuses
- REST API endpoint to identify GSTINs that haven't filed GSTR-1 or GSTR-3B for the current month

## Tech Stack

- Python / Django 6
- Django REST Framework
- SQLite

## Setup

```bash
python -m venv venv
source venv/Scripts/activate  # Windows
pip install django djangorestframework

python manage.py migrate
python manage.py runserver
```

## API

### `GET /api/unfiled-gstins/`

Returns all active onboarded GSTINs that have not filed GSTR-1 or GSTR-3B for the current month.

**Example**
```bash
curl http://127.0.0.1:8000/api/unfiled-gstins/
```

**Response**
```json
{
  "period": "Mar-2026",
  "count": 3,
  "results": [
    {
      "gstin": "27AABCU9603R1ZX",
      "business_name": "Acme Traders",
      "admin_email": "admin@acmetraders.com",
      "period": "Mar-2026",
      "missing_returns": ["GSTR1", "GSTR3B"]
    }
  ]
}
```

## Models

**`OnboardedGSTIN`** — Registered businesses tracked in the system

| Field | Type | Description |
|-------|------|-------------|
| gstin | CharField (15) | Unique GSTIN number |
| trade_name | CharField | Business trade name |
| legal_name | CharField | Legal entity name |
| state | CharField | State of registration |
| admin_email | EmailField | Admin contact email |
| is_active | BooleanField | Whether the GSTIN is active |

**`GSTINFilingStatus`** — Filing records per GSTIN per period

| Field | Type | Description |
|-------|------|-------------|
| gstin | ForeignKey | Linked OnboardedGSTIN |
| return_type | CharField | GSTR1, GSTR3B, or GSTR9 |
| period | CharField | e.g. `Jan-2026` |
| status | CharField | Filed, Not Filed, or Pending |
| filed_date | DateField | Date filed (nullable) |
| due_date | DateField | Filing due date |
