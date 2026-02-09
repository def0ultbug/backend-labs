# FastAPI Authentication System 🔐

A comprehensive RESTful API built with FastAPI demonstrating **advanced authentication and authorization patterns**. This project implements OAuth2, JWT, MFA, RBAC, and third-party authentication for learning modern security practices.

## ⚠️ Important Note for Reviewers

This project is a **learning exercise**. Its purpose is to practice modern authentication and authorization techniques, including:
- OAuth2 with JWT tokens
- Multi-factor authentication (MFA)
- Role-Based Access Control (RBAC)
- Third-party OAuth (GitHub)
- API key authentication
- Session management

**Not production-ready:**
- Educational implementation of security concepts
- Simplified error handling
- Basic database setup (SQLite)
- Demonstration purposes only

Please evaluate it in the context of **learning and experimentation**, not production code.

## 🎯 Project Purpose

This mini-project focuses on learning and implementing:
- **OAuth2 Protocol** - Industry-standard authorization framework
- **JSON Web Tokens (JWT)** - Secure token-based authentication
- **Multi-Factor Authentication (MFA)** - Additional security layer with TOTP
- **Role-Based Access Control (RBAC)** - Permission management system
- **Third-Party Authentication** - GitHub OAuth integration
- **API Key Authentication** - Alternative authentication method
- **Session Management** - Cookie-based sessions and logout functionality
- **User Registration** - Multiple user tier registration flows

## ✨ Features

- 🔑 **OAuth2 & JWT** - Secure token-based authentication
- 🛡️ **Multi-Factor Authentication** - TOTP-based MFA for enhanced security
- 👥 **User Registration** - Basic and premium user tiers
- 🎭 **RBAC Implementation** - Role-based access control
- 🐙 **GitHub OAuth** - Third-party authentication integration
- 🔐 **API Key Authentication** - Alternative authentication method
- 🍪 **Session Management** - Cookie-based sessions with logout
- 🚪 **Secure Resources** - Protected endpoints requiring authentication
- ✅ **Data Validation** - Robust validation using Pydantic models

## 🗂️ Project Structure

```
03_fastapi_security/
├── 03_fastapi_security/
│   ├── __init__.py
│   ├── main.py                      # FastAPI app entry point
│   ├── models.py                    # SQLAlchemy database models
│   ├── database.py                  # Database configuration
│   ├── database.db                  # SQLite database file
│   ├── operations.py                # User CRUD operations
│   ├── auth_utils.py                # JWT and authentication utilities
│   ├── rbac.py                      # Role-based access control
│   ├── mfa.py                       # Multi-factor authentication
│   ├── api_key.py                   # API key authentication
│   ├── github_login.py              # GitHub OAuth routes
│   ├── github_auth_operations.py    # GitHub auth operations
│   ├── premium_access.py            # Premium user routes
│   ├── user_session.py              # Session management
│   ├── Responses.py                 # Response schemas
│   └── test_operations.py           # Testing scripts
├── tests/
│   └── __init__.py                  # Test files (to be implemented)
├── pyproject.toml                   # Poetry dependencies
├── poetry.lock                      # Locked dependencies
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Poetry (for dependency management)

### Installation

#### Using Poetry
```bash
# Navigate to project directory
cd fastapi_auth

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### Running the Application
```bash
# Start the development server
python -m fastapi_auth.main

# Or run directly
python fastapi_auth/main.py

# The API will be available at:
# http://localhost:8000

# Interactive API documentation:
# http://localhost:8000/docs (Swagger UI)
# http://localhost:8000/redoc (ReDoc)
```

## 📡 API Endpoints

### Authentication & Authorization

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/token/create` | Get User Access Token (JWT) | No |
| `POST` | `/login` | User login with credentials | No |
| `POST` | `/logout` | Logout and invalidate session | Yes 🔒 |
| `GET` | `/users/me` | Read current user profile | Yes 🔒 |

### User Registration

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/register/basic_user` | Register as basic user | No |
| `POST` | `/register/premium-user` | Register as premium user | No |

### Access Control (RBAC)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/welcome/all-users` | Access for all authenticated users | Yes 🔒 |
| `POST` | `/welcome/premium-user` | Access for premium users only | Yes 🔒 (Premium) |
| `GET` | `/secure-resources` | Access secure resources | Yes 🔒 |
| `GET` | `/home` | Public homepage | No |

### Multi-Factor Authentication (MFA)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/user/enable-mfa` | Enable MFA for user account | Yes 🔒 |
| `POST` | `/verify-MFA-code` | Verify MFA code | Yes 🔒 |

### Third-Party Authentication (GitHub)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/auth/url` | Get GitHub OAuth URL | No |
| `GET` | `/github/auth/token` | OAuth callback handler | No |

## 🔐 Authentication Methods

### 1. JWT Token Authentication
```bash
# Get access token
curl -X POST "http://localhost:8000/token/create" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=yourpassword"

# Use token in requests
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://localhost:8000/users/me
```

### 2. Session Cookie Authentication
```bash
# Login (sets session cookie)
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "yourpassword"}'

# Logout (clears session)
curl -X POST "http://localhost:8000/logout" \
  --cookie "session_id=YOUR_SESSION_ID"
```

### 3. API Key Authentication
```bash
# Access with API key
curl -H "X-API-Key: YOUR_API_KEY" \
  http://localhost:8000/secure-resources
```

## 📝 Example Usage

### Register a New User
```bash
# Register basic user
curl -X POST "http://localhost:8000/register/basic_user" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123",
    "username": "johndoe"
  }'

# Register premium user
curl -X POST "http://localhost:8000/register/premium-user" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "premium@example.com",
    "password": "securepassword123",
    "username": "janedoe"
  }'
```

### Enable Multi-Factor Authentication
```bash
# Step 1: Enable MFA (returns QR code)
curl -X POST "http://localhost:8000/user/enable-mfa" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Step 2: Verify MFA code
curl -X POST "http://localhost:8000/verify-MFA-code" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "123456"
  }'
```

### Access Protected Resources
```bash
# Access all-users endpoint
curl -X POST "http://localhost:8000/welcome/all-users" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Access premium-only endpoint
curl -X POST "http://localhost:8000/welcome/premium-user" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### GitHub OAuth Flow
```bash
# Step 1: Get GitHub OAuth URL
curl -X POST "http://localhost:8000/auth/url"

# Step 2: User authorizes on GitHub and is redirected to callback
# GET /github/auth/token?code=GITHUB_CODE
```

## 🔒 Security Features

### OAuth2 with JWT
- **Access Tokens**: Short-lived JWT tokens for API access
- **Token Expiration**: Configurable token lifetime
- **Secure Password Hashing**: bcrypt for password storage

### Multi-Factor Authentication
- **TOTP-based**: Time-based One-Time Passwords
- **QR Code Generation**: Easy setup with authenticator apps
- **Backup Codes**: Recovery options (can be implemented)

### Role-Based Access Control
- **User Roles**: Basic user, Premium user, Admin
- **Permission Management**: Endpoint-level access control
- **Resource Protection**: Automatic authorization checks

### Third-Party OAuth
- **GitHub Integration**: OAuth 2.0 flow
- **Secure Callbacks**: Token exchange and validation
- **User Linking**: Connect GitHub accounts to local users

## 📚 API Documentation

### Swagger UI
Visit `http://localhost:8000/docs` for interactive API testing with:
- Visual endpoint exploration
- Authentication testing
- Request/response examples
- Schema definitions
- Try-it-out functionality

### ReDoc
Visit `http://localhost:8000/redoc` for comprehensive documentation:
- Clean, readable interface
- Detailed endpoint descriptions
- Authentication flows
- Model schemas

## 🎓 What I Learned

- ✅ Implementing OAuth2 authorization framework
- ✅ Working with JSON Web Tokens (JWT)
- ✅ Building multi-factor authentication (TOTP)
- ✅ Designing role-based access control systems
- ✅ Integrating third-party OAuth providers (GitHub)
- ✅ Managing API key authentication
- ✅ Handling session cookies and logout
- ✅ Securing endpoints with dependency injection
- ✅ Password hashing and validation
- ✅ Token refresh strategies
- ✅ User registration workflows
- ✅ Database modeling for authentication

## 🛠️ Technologies Used

- **FastAPI** - Modern, fast web framework for building APIs
- **OAuth2** - Industry-standard authorization framework
- **JWT (JSON Web Tokens)** - Secure token-based authentication
- **SQLAlchemy** - Python SQL toolkit and ORM
- **SQLite** - Lightweight database for development
- **Pydantic** - Data validation using Python type annotations
- **PyOTP** - Python One-Time Password library for MFA
- **Passlib** - Password hashing library
- **Python-Jose** - JWT implementation
- **HTTPX** - HTTP client for OAuth callbacks
- **Uvicorn** - ASGI server for running FastAPI
- **Poetry** - Dependency management

## 🐛 Known Limitations

- **Development Database** - SQLite not suitable for production
- **Simplified Error Handling** - Basic error responses
- **No Token Refresh** - Access tokens expire without refresh mechanism
- **No Email Verification** - Email confirmation not implemented
- **Basic RBAC** - Simple role system without complex permissions
- **No Rate Limiting** - API calls not rate-limited
- **Session Storage** - In-memory session storage (not persistent)
- **MFA Backup Codes** - Recovery codes not implemented
- **No Account Recovery** - Password reset flow not included
- **Limited OAuth Providers** - Only GitHub implemented

## 🔧 Configuration

### Environment Variables (Example)
```env
# JWT Configuration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# GitHub OAuth
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
GITHUB_REDIRECT_URI=http://localhost:8000/github/auth/token

# Database
DATABASE_URL=sqlite:///./database.db
```

## 📖 Authentication Flow

### Standard Login Flow
1. User registers with email/password
2. User logs in with credentials
3. Server validates and returns JWT token
4. Client includes token in subsequent requests
5. Server validates token on protected endpoints

### MFA Flow
1. User enables MFA
2. Server generates TOTP secret and QR code
3. User scans QR code with authenticator app
4. User enters verification code
5. Server validates and confirms MFA setup
6. Future logins require both password and MFA code

### GitHub OAuth Flow
1. Client requests GitHub OAuth URL
2. User authorizes on GitHub
3. GitHub redirects to callback with code
4. Server exchanges code for access token
5. Server fetches user info from GitHub
6. Server creates/links local user account
7. Server returns JWT token to client

## 📄 License

MIT License - Free to use for learning purposes.

---

**Part of:** Backend Development Learning Journey 🚀

💡 **Learning Focus:** Mastering authentication, authorization, OAuth2, JWT, MFA, RBAC, and security best practices in modern web applications.

## 🤝 Contributing

This is a learning project, but feedback and suggestions are welcome! Feel free to:
- Open issues for bugs or suggestions
- Submit pull requests for improvements
- Share your learning experience
- Suggest additional authentication methods to explore

## 📚 Additional Resources

- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/)
- [OAuth 2.0 Specification](https://oauth.net/2/)
- [JWT Introduction](https://jwt.io/introduction)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)

---

*Built with ❤️ while learning modern authentication and security practices with FastAPI*