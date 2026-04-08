# Standard Hugging Face Spaces Dockerfile
FROM python:3.11-slim

# Set up a new user (Hugging Face requires this for security)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set the working directory
WORKDIR $HOME/app

# Copy your files into the container
COPY --chown=user . $HOME/app

# Install the required packages
# Forcibly install all required packages to prevent missing requirements errors
RUN pip install --no-cache-dir fastapi uvicorn pydantic openai numpy

# Standard Hugging Face FastAPI execution method
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
