# FROM python:3.13.11-slim-bookworm
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# COPY app.py .
# ENV PORT=8080
# EXPOSE 8080
# CMD ["fastapi" , "run"]

# Stage 1: The Build Environment
FROM python:3.11-slim AS builder
# 1. Install uv
# uv is installed globally in this stage for use in the build
RUN pip install uv

# Set environment variables for the build
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


# 2. Copy project files needed for dependency resolution
WORKDIR /app
COPY requirements.txt .

# 3. Create the venv and install dependencies using uv
# --no-deps ensures that uv uses the cache/lockfile efficiently.
# --system-site-packages is not used, keeping the venv clean.

# RUN uv venv --system-site-packages # We use the standard library copy of certifi, etc.
RUN uv venv /opt/venv 
RUN uv pip install -r requirements.txt

# Stage 2: The Final Runtime Environment
# We use a minimal base image that matches the 'builder' stage for compatibility
# FROM python:3.12-slim AS final
FROM gcr.io/distroless/python3 AS final

# 1. Define Environment Variables for the Runtime
# These variables tell Python and the OS where to find the VENV
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# 2. Copy the VENV from the builder stage
# This is the magic of the multistage build: only the built VENV is moved
ENV PYTHON_VERSION 3.11
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /opt/venv /usr/local/lib/python${PYTHON_VERSION}/site-packages
# 3. Copy the Application Code
WORKDIR /app
COPY app.py .
COPY settings.py .
# COPY your_project_folder/ ./your_project_folder/ # Adjust for your project structure

# 4. Set the startup command
# Use the python executable from the copied VENV
CMD [ "app.py"]
# CMD ["/opt/venv/python","app.py"]
