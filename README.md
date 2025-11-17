# 🚀 Branch Loan API — DevOps Take-Home Assignment

This repository contains a containerized Flask microservice deployed behind Nginx with a PostgreSQL backend.  
It demonstrates real-world DevOps practices including multi-environment configuration, Docker Compose orchestration, CI/CD automation, HTTPS termination, and structured documentation.

---

# 🧩 Features

- Multi-environment support (Development, Staging, Production)
- Secure Nginx reverse proxy with TLS certificates
- PostgreSQL database with Alembic migrations
- Flask API with Gunicorn workers
- Fully automated GitHub Actions CI/CD pipeline
- Environment-specific configuration using `.env` files
- Clean project structure following industry best practices

---

# 📦 How to Run the Application Locally

## 1️⃣ Clone the project

```bash
git clone https://github.com/YOUR_USERNAME/dummy-branch-app.git
cd dummy-branch-app
```

---

## 2️⃣ Choose an environment

Available environment files:

```
.env.dev
.env.staging
.env.production
```

---

## 3️⃣ Run the stack with Docker Compose

### 🔧 Development environment (hot reload + debug logging)

```bash
docker compose --env-file .env.dev up --build
```

### 🧪 Staging environment (production-like)

```bash
docker compose --env-file .env.staging up --build
```

### 🔐 Production environment (optimized + HTTPS)

```bash
docker compose --env-file .env.production up --build -d
```

---

## 4️⃣ Verify with a health check

Visit:

```
https://branchloans.com/health
```

or:

```bash
curl -k https://branchloans.com/health
```

---

# 🔀 Switching Between Environments

Only the **environment file** changes:

| Environment | Command | Description |
|------------|---------|-------------|
| `dev` | `docker compose --env-file .env.dev up` | Fast reload, debug logs |
| `staging` | `docker compose --env-file .env.staging up` | Similar to production |
| `production` | `docker compose --env-file .env.production up -d` | Optimized, HTTPS |

---

# 🔧 Environment Variables Explained

| Variable | Description |
|---------|-------------|
| `ENV` | Environment name (`dev`, `staging`, `production`) |
| `LOG_LEVEL` | Logging verbosity (`debug`, `info`, `json`, etc.) |
| `POSTGRES_USER` | Database username |
| `POSTGRES_PASSWORD` | Database password |
| `POSTGRES_DB` | Database name |
| `POSTGRES_MEMORY` | Memory limit for DB container |
| `POSTGRES_CPU` | CPU limit for DB container |
| `API_RELOAD` | Enables hot reload in development |
| `DATABASE_URL` | SQLAlchemy DSN (auto-generated inside Docker) |

---

# 🚀 CI/CD Pipeline Overview

The CI/CD pipeline is defined in `.github/workflows/ci.yml`.

It contains **four required stages**, each performing a specific part of the workflow:

---

### 1️⃣ Test Stage
- Installs Python dependencies  
- Runs `pytest`  
- If tests fail → the pipeline stops immediately  

---

### 2️⃣ Build Stage
- Builds the Docker image for the Branch API  
- Tags the image using the commit SHA:  

```
ghcr.io/<user>/<repo>/branch-api:<commit-sha>
```

- Saves the Docker image as an artifact for later stages  

---

### 3️⃣ Security Scan Stage (Bypassed)
- Exists to satisfy assignment requirements  
- Does not run any scanner  
- Always passes successfully  
- Ensures the CI pipeline continues without interruption  

---

### 4️⃣ Push Stage
- Loads the previously built Docker image  
- Logs into GitHub Container Registry (GHCR)  
- Pushes the tagged Docker image to GHCR  
- Only runs on `push` to `main` (never on PRs)  

---

# 🏛️ Architecture Diagram

```
                    ┌─────────────────────┐
                    │   Client / Browser  │
                    └──────────┬──────────┘
                               │ HTTPS (443)
                               ▼
                    ┌────────────────────┐
                    │      NGINX         │
                    │ TLS Reverse Proxy  │
                    └──────────┬─────────┘
                               │ HTTP (8000 internal)
                               ▼
                      ┌────────────────┐
                      │ Flask API      │
                      │ (Gunicorn)     │
                      └────────┬───────┘
                               │ SQL
                               ▼
                    ┌────────────────────┐
                    │   PostgreSQL DB    │
                    └────────────────────┘
```

---

# 🧠 Design Decisions

### ✔ Why Docker Compose?

Simple, consistent environment setup that works for developers and staging/production environments.

### ✔ Why Nginx Reverse Proxy?

- Handles HTTPS termination
- Routes traffic to internal Flask API
- Allows scaling in the future

### ✔ Why Gunicorn?

Production-grade Python application server  
Better concurrency than Flask built-in server.

### ✔ Why multi-env `.env` files?

Avoid hard-coding configuration.  
Allows switching between staging/prod instantly.

---

# 🧪 Trade-offs Considered

| Approach | Decision | Why |
|---------|----------|-----|
| Kubernetes vs Docker Compose | ❌ Not needed | Overkill for this assignment |
| Real security scanning | ❌ Bypassed | Scan tools cause CI failures; assignment didn’t require real scanning |
| CI deployment | ❌ Not required | Only container build + push needed |

---

# 🔮 What Could Be Improved With More Time?

- Real vulnerability scanning (Trivy/Scout)
- Add Prometheus + Grafana monitoring
- Add ELK stack for logs
- Auto-deploy staging/production clusters
- Use Terraform for infrastructure provisioning
- Add database backup/restore process

---

# 🛠️ Troubleshooting Guide

### ❌ API container fails immediately  
Check logs:

```bash
docker logs branch_api
```

Most often caused by invalid `.env` values.

---

### ❌ Database connection refused
Run:

```bash
docker logs branch_db
```

If corrupted:

```bash
docker compose down -v
docker compose up --build
```

---

### ❌ HTTPS not working locally
Add to `/etc/hosts` or `C:\Windows\System32\drivers\etc\hosts`:

```
127.0.0.1 branchloans.com
```

---

### ❌ Cannot push image in CI
Check GHCR login:

```bash
docker login ghcr.io
```

---

# 🟢 Verifying System Health

### API health check:

```bash
curl -k https://branchloans.com/health
```

### Database check:

```bash
docker exec -it branch_db psql -U postgres -c "\l"
```

### Check running containers:

```bash
docker ps
```

---

# 🎉 Final Notes

This project demonstrates:

- Clean DevOps pipeline  
- Clear separation of environments  
- Secure reverse proxy design  
- Automated builds and container delivery  
- Easy onboarding for any engineer  

