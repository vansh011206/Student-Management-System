import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

username = os.environ.get('ADMIN_USERNAME', 'admin')
password = os.environ.get('ADMIN_PASSWORD', 'Admin@12345')
email    = os.environ.get('ADMIN_EMAIL', 'admin@edumanage.com')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        role='admin'
    )
    print(f"[OK] Superuser '{username}' created successfully")
else:
    print(f"[INFO] Superuser '{username}' already exists - skipping")
