#!/usr/bin/env bash
# Render build script
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Create superuser if it doesn't exist (uses env vars DJANGO_SUPERUSER_*)
if [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
    python manage.py createsuperuser --no-input 2>/dev/null || echo "Superuser already exists, skipping."
    # Always force-update the password to ensure it matches env var
    python manage.py shell -c "
from django.contrib.auth.models import User
import os
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
try:
    u = User.objects.get(username=username)
    u.set_password(password)
    u.save()
    print(f'Password updated for {username}')
except User.DoesNotExist:
    print(f'User {username} not found')
"
fi
