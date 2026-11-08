# syntax=docker/dockerfile:1

# ---------- Stage 1: builder ----------
# Installs dependencies into an isolated virtualenv. Anything needed only to
# build (pip caches, compilers if a dependency ever needs them) stays in this
# stage and never reaches the final image.
# Base image is pinned by digest for reproducible builds; Dependabot bumps it.
FROM python:3.12-slim@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /build
COPY requirements.txt .
RUN pip install -r requirements.txt

# ---------- Stage 2: runtime ----------
FROM python:3.12-slim@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b AS runtime

# CI passes the git commit SHA here, so every running pod reports exactly
# which commit it was built from (GET / -> "version").
ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION} \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Fixed numeric UID/GID so Kubernetes can verify runAsNonRoot.
RUN groupadd --gid 10001 appuser \
 && useradd --uid 10001 --gid 10001 --no-create-home --shell /usr/sbin/nologin appuser

WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY main.py .

USER 10001
EXPOSE 8080

# Gunicorn is a production WSGI server; Flask's built-in server is for
# development only. Exec form makes gunicorn PID 1, so it receives SIGTERM
# from Kubernetes directly and shuts down gracefully.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--access-logfile", "-", "main:app"]
