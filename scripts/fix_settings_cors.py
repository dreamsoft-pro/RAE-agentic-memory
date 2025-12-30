import os

target_path = "/home/grzegorz-lesniowski/cloud/screenwatcher_project/screenwatcher_project/settings.py"

with open(target_path, 'r') as f:
    content = f.read()

# 1. Disable SSL Redirect for Dev
content = content.replace("SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=True)", 
                          "SECURE_SSL_REDIRECT = False # Disabled for local dev")

# 2. Add CORS Headers
if "'corsheaders'," not in content:
    content = content.replace("'daphne',", "'daphne',\n    'corsheaders',")

if "'corsheaders.middleware.CorsMiddleware'," not in content:
    content = content.replace("'django.middleware.security.SecurityMiddleware',", 
                              "'django.middleware.security.SecurityMiddleware',\n    'corsheaders.middleware.CorsMiddleware',")

# 3. Add CORS Config at the end
cors_config = """
# CORS Settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
"""
if "CORS_ALLOW_ALL_ORIGINS" not in content:
    content += cors_config

with open(target_path, 'w') as f:
    f.write(content)

print("Updated settings.py: Disabled SSL Redirect and added CORS headers.")