# Bookmark Service API

A resilient HTTP service for managing bookmarks with strict input validation, graceful error handling, and guaranteed idempotency.

**Built for:** Verified Backend Internship (Task: API that survives malformed input)

---

## Overview

This API provides a robust bookmark management system that rejects invalid payloads at the boundary, prevents duplicate entries, and ensures consistent behavior across all request types. No unhandled errors—only meaningful validation feedback.

---

## API Endpoints

| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| POST | `/bookmarks` | Create a bookmark or fetch existing | 201 Created / 200 OK / 400 Bad Request |
| GET | `/bookmarks` | List all bookmarks (descending order) | 200 OK |
| GET | `/bookmarks/{id}` | Fetch bookmark by ID | 200 OK / 404 Not Found |
| DELETE | `/bookmarks/{id}` | Delete bookmark by ID | 204 No Content / 404 Not Found |

---

## Input Validation

All requests are validated before database operations. Invalid input returns `400 Bad Request` with a clear error message.

### Validation Rules

- **URL Required**: Field cannot be empty or null
- **Valid Data Type**: Must be a string (not number, boolean, or object)
- **URL Length**: Maximum 2048 characters
- **Protocol Required**: Must start with `http://` or `https://`

### Error Response Example

```json
{
  "error": "Invalid field 'url': Field required",
  "field": "url"
}
```

---

## Idempotency & Duplicate Prevention

Sending the same bookmark twice produces only one database entry.

### How It Works

1. **Normalization**: URLs are trimmed of leading/trailing whitespace
2. **Duplicate Check**: Before inserting, the service queries for an existing matching URL
3. **First Request**: Returns `201 Created` with the new bookmark ID
4. **Repeat Request**: Returns `200 OK` with the existing bookmark (no duplicate created)
5. **Database Layer**: `UNIQUE` constraint on the `url` column prevents concurrent race conditions

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd bookmark-service
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python -m uvicorn main:app --reload
```

4. View interactive API documentation:
```
http://127.0.0.1:8000/docs
```

---

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite
- **Validation**: Pydantic

---

## Error Handling

The service handles edge cases gracefully and never returns unhandled `500` errors. All client errors return `400 Bad Request` with identifying information. All server resources return appropriate status codes.

---

## License

This project is licensed as personal property.
