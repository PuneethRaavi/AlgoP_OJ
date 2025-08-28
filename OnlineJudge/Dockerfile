# Use Python as base
FROM python:3.9

# Prevent Python from buffering logs
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=OnlineJudge.settings

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    default-jdk \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /algop_oj

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /algop_oj

# Run collectstatic to gather all static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Set the command to run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "OnlineJudge.wsgi:application"]