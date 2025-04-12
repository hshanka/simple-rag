# Stage 1: Builder stage using an image with build tools.
FROM python:3.9-slim AS builder
WORKDIR /app

# Install system build tools.
RUN apt-get update && apt-get install -y build-essential

# Upgrade pip.
RUN python -m pip install --upgrade pip

# Build wheels for the required packages.
# This builds wheels for: openai, langchain_community, langchain_openai, pypdf, chromadb, and aiosignal.
RUN python -m pip wheel --no-cache-dir openai langchain_community langchain_openai pypdf chromadb aiosignal

# Stage 2: Final stage using the Chainguard Python base image (latest-dev).
FROM cgr.dev/chainguard/python:latest-dev
WORKDIR /app

# Bootstrap and upgrade pip.
RUN ["python", "-m", "ensurepip"]
RUN ["python", "-m", "pip", "install", "--upgrade", "pip"]

# Copy the pre-built wheels from the builder stage.
COPY --from=builder /app/*.whl /app/

# Install all compatible wheels except those for aiosignal.
RUN ["python", "-c", "import glob, os, subprocess, sys; [print('Installing', w) or subprocess.call(['python', '-m', 'pip', 'install', '--no-cache-dir', w]) for w in sorted(glob.glob('/app/*.whl')) if 'aiosignal' not in os.path.basename(w).lower()]; sys.exit(0)"]

# Install aiosignal separately to ensure a compatible version.
RUN ["python", "-m", "pip", "install", "--no-cache-dir", "aiosignal==1.3.2"]

# Copy your application script and PDF files.
COPY pdfrag.py .
COPY *.pdf .

# Clear the default ENTRYPOINT and run your script.
ENTRYPOINT []
CMD ["python", "pdfrag.py"]