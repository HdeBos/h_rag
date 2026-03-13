# ── Stage 1: dependency builder ──────────────────────────────────────────────
FROM python:3.13.12-slim-bookworm AS builder

# Install UV
COPY --from=docker.io/astral/uv:latest /uv /uvx /bin/

# Set the working directory
WORKDIR /app

# Compile .pyc files at install time; copy package files instead of symlinking
# so the venv is fully self-contained when copied to the runtime image.
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --no-install-project


# Copy source and install the project itself
COPY . .
RUN uv sync --no-dev

# ── Stage 2: runtime image ────────────────────────────────────────────────────
FROM python:3.13.12-slim-bookworm AS runtime


# libgomp1  – OpenMP runtime required by PyTorch (sentence-transformers) and
#             onnxruntime (chromadb default embedding function).
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy the virtual environment from the builder
COPY --from=builder /app /app

# Activate the venv and keep Python output unbuffered for clean log streaming.
ENV PATH="/app/.venv/bin:$PATH"
# ENV PYTHONUNBUFFERED=1

EXPOSE 8000

WORKDIR /app

CMD ["fastapi", "dev", "--host", "0.0.0.0"]
