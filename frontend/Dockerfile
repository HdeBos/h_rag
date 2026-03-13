# ── Stage 1: dependency builder ──────────────────────────────────────────────
FROM python:3.13.12-slim-bookworm AS builder

# Install UV
COPY --from=docker.io/astral/uv:latest /uv /uvx /bin/

# Set the working directory
WORKDIR /app

# Install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --no-install-project

# Copy source and install the project itself
COPY . .
RUN uv sync --no-dev

# ── Stage 2: runtime image ────────────────────────────────────────────────────
FROM python:3.13.12-slim-bookworm AS runtime

# Copy the virtual environment from the builder
COPY --from=builder /app /app

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Expose the default Streamlit port
EXPOSE 8501

WORKDIR /app

# Run the application
ENTRYPOINT ["streamlit", "run", "src/h_rag/chat.py"]