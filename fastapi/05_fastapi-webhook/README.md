# FastAPI ASGI Middleware & Webhooks 🔗

A focused deep-dive into **ASGI middleware** and **webhook systems** built with FastAPI. This project demonstrates how to intercept and modify HTTP requests/responses at the middleware level, enforce host restrictions, handle CORS, and implement a fully functional webhook notification system.

## ⚠️ Note for Reviewers

This is a **learning project** focused on understanding low-level ASGI internals and middleware patterns. It is not production-ready:
- Webhook URLs are stored in application state (in-memory), not a database
- No authentication or authorization
- Minimal error handling

Please evaluate it as a **hands-on exploration** of FastAPI middleware and webhook architecture.

---

## 🎯 Project Purpose

This project focuses on learning and implementing:
- **Custom ASGI middleware** — building middleware from scratch using the ASGI interface (`scope`, `receive`, `send`)
- **Request modification middleware** — intercepting and reading request data before it reaches route handlers
- **Response modification middleware** — intercepting and altering responses before they are sent back to the client
- **CORS handling** — managing cross-origin resource sharing at the middleware level
- **Host restriction** — blocking or allowing requests based on the client's host
- **Webhooks** — implementing a subscriber/notification system where registered clients get notified on every API call

---

## ✨ Features

- 🔧 **Custom ASGI Middleware** — low-level middleware using `scope`, `receive`, and `send` directly
- 📨 **Request Middleware** — reads and logs request body, path, host, and timestamp
- 📤 **Response Middleware** — intercepts response before it reaches the client
- 🌐 **CORS Middleware** — handles cross-origin requests
- 🚫 **Host Restriction** — blocks requests from untrusted hosts
- 🔔 **Webhook System** — clients register a URL and get notified via HTTP POST on every API call
- 📖 **Webhook Documentation** — uses `app.webhooks` to document the event payload shape in Swagger UI

---

## 🗂️ Project Structure

```
05_fastapi_webhook/
├── 05_fastapi_webhook/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point, middleware registration & lifespan
│   ├── asgi_middleware.py   # Custom ASGI middleware (request, response, CORS, host restriction)
│   └── webhook.py           # Webhook registration endpoint, Event model & sender logic
├── pyproject.toml           # Poetry dependencies and project config
├── poetry.lock              # Locked dependencies
├── README.md
└── tests/
    └── __init__.py
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Poetry

### Installation

```bash
# Navigate to project directory
cd 05_fastapi_webhook

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### Running the Application

```bash
python -m 05_fastapi_webhook.main

# API available at:
# http://localhost:8000

# Swagger UI (interactive docs):
# http://localhost:8000/docs

# ReDoc:
# http://localhost:8000/redoc
```

---

## 🔔 How the Webhook System Works

```
1. Client registers their URL
   POST /register-webhook-url
   Body: "https://client-site.com/notify"

2. URL is stored in app state (in-memory set)

3. Any API call is made to this server

4. WebhookSenderMiddleWare intercepts the request

5. An Event is built (host, path, timestamp, body)

6. HTTP POST is sent to every registered URL with the Event payload
```

### Event Payload

When a registered client is notified, they receive a POST request with this JSON body:

```json
{
  "host": "127.0.0.1",
  "path": "/some-endpoint",
  "time": "2024-05-22T14:24:28.847663",
  "body": "request body content"
}
```

### Example: Register a Webhook URL

```bash
curl -X POST "http://localhost:8000/register-webhook-url" \
  -H "Content-Type: application/json" \
  -d '"https://your-site.com/webhook-handler"'
```

---

## 🧱 Middleware Overview

### `WebhookSenderMiddleWare`
Fires on every HTTP request. Reads the request, builds an `Event` object, and asynchronously notifies all registered webhook URLs before passing the request to the actual route handler.

> **Key detail:** Since `receive()` can only be read once, the middleware wraps the already-read body in a `continue_receive()` function so the route handler still has access to the body.

### CORS Middleware
Handles `Access-Control-Allow-*` headers for cross-origin requests.

### Host Restriction Middleware
Inspects the incoming request's host and blocks requests from hosts that are not on the allowlist, returning a `403 Forbidden` response.

### Response Modification Middleware
Intercepts the response before it is sent to the client, allowing headers or body content to be modified.

---

## 🔄 In-Memory vs Database Storage

This project stores webhook URLs in application state (a Python `set` in memory):

| Approach | Pros | Cons |
|----------|------|------|
| **In-memory (this project)** | Simple, no setup needed | Lost on server restart |
| **Database** | Persistent, production-ready | Requires DB setup |

Using a `set` (rather than a list) ensures duplicate URLs are automatically ignored — if a client registers the same URL twice, they only get notified once per event.

---

## 🎓 What I Learned

- ✅ How ASGI works at a low level (`scope`, `receive`, `send`)
- ✅ Building custom middleware classes from scratch
- ✅ Reading request body in middleware without breaking the route handler
- ✅ Storing and sharing state across requests using FastAPI lifespan
- ✅ Implementing a webhook subscriber/notification pattern
- ✅ Documenting webhooks with `app.webhooks` in Swagger UI
- ✅ Handling CORS and host-based access control at the middleware level
- ✅ Async HTTP calls with `httpx.AsyncClient`

---

## 🛠️ Technologies Used

- **FastAPI** — modern async web framework
- **Pydantic** — data validation and webhook event schema
- **HTTPX** — async HTTP client for sending webhook notifications
- **Uvicorn** — ASGI server
- **Poetry** — dependency management

---

## 🐛 Known Limitations

- **In-memory storage** — registered webhook URLs are lost on server restart
- **No authentication** — any client can register a URL
- **No retry logic** — if a webhook delivery fails, it is not retried
- **No filtering** — all subscribers are notified for every API call, not per event type
- **No concurrency control** — simultaneous writes to the URL set are not protected

---

## 📄 License

MIT License — free to use for learning purposes.

---

**Part of:** Backend Development Learning Journey 🚀

💡 **Learning Focus:** Mastering ASGI internals, custom middleware patterns, and event-driven webhook architecture with FastAPI.

*Built with ❤️ while learning low-level FastAPI and async Python*
