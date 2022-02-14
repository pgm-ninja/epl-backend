from .env_config import CURRENT_ENVIRONMENT
import os
import django


def get_django_setting_module():
    if CURRENT_ENVIRONMENT == "Local":
        return "core.settings.environments.local.local"
    if CURRENT_ENVIRONMENT == "Staging":
        return "core.settings.environments.staging.staging"
    if CURRENT_ENVIRONMENT == "Production":
        return "core.settings.environments.production.production"


def django_setup():
    os.environ['DJANGO_SETTINGS_MODULE'] = get_django_setting_module()
    django.setup()
