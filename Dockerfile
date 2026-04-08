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
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Start the FastAPI server on port 7860 (Hugging Face standard)
CMD ["python", "app.py"]
