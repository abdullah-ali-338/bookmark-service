# 📌 Bookmark Service API

![Python Version](https://img.shields.io/badge/Language-Python_3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-Personal_Use-blue?style=for-the-badge)
![Tech Stack](https://img.shields.io/badge/Stack-FastAPI_%7C_SQLite_%7C_Pydantic-orange?style=for-the-badge)

A resilient HTTP service for managing bookmarks with strict input validation, graceful error handling, and guaranteed idempotency.

🌐 **GitHub Repo:** [github.com/abdullah-ali-338/bookmark-service-api](https://github.com/abdullah-ali-338/bookmark-service-api)

---

## ✨ Features

- **Boundary Validation:** Rejects malformed payloads before hitting the database, enforcing strict URL schema, protocol, length, and data type checks via Pydantic.
- **Guaranteed Idempotency:** Normalizes incoming URLs and checks for duplicates prior to insertion, returning existing records gracefully without creating redundant entries.
- **Race Condition Prevention:** Database-level `UNIQUE` constraints prevent concurrent duplication under heavy traffic.
- **Graceful Error Handling:** Eliminates unhandled 500 internal errors by returning structured, field-specific 400 Bad Request responses.

---

## 🛠️ Tech Stack

- **Framework:** FastAPI
- **Database:** SQLite
- **Validation Engine:** Pydantic
- **Server:** Uvicorn ASGI

---

## 📁 Repository Structure

```text
BookmarkService/
├── main.py             # FastAPI endpoints, routes, and error handlers
├── database.py         # SQLite connection setup and table schema
├── schemas.py          # Pydantic models and input validation rules
├── requirements.txt    # Python dependencies
└── README.md           # Documentation
