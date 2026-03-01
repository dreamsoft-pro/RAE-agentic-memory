from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from apps.audit.models import AuditLog
from apps.audit.middleware import get_current_user, get_current_ip
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.apps import apps
from django.forms.models import model_to_dict
import json

# Models to track for ISO 27001 compliance
TRACKED_MODELS = [
    'auth.User',
    'registry.Machine',
    'registry.Line',
    'registry.Factory',
    'rules.Rule',
]

def get_model_changes(instance):
    """
    Compares the current instance with its database state and returns a dict of changes.
    """
    if not instance.pk:
        return {}
    
    try:
        old_instance = instance.__class__.objects.get(pk=instance.pk)
    except instance.__class__.DoesNotExist:
        return {}

    old_dict = model_to_dict(old_instance)
    new_dict = model_to_dict(instance)
    
    changes = {}
    for field, value in new_dict.items():
        old_value = old_dict.get(field)
        if value != old_value:
            changes[field] = {
                'old': str(old_value) if old_value is not None else None,
                'new': str(value) if value is not None else None
            }
    return changes

def audit_pre_save(sender, instance, **kwargs):
    """Capture changes before saving."""
    if instance.pk:
        instance._audit_changes = get_model_changes(instance)
    else:
        instance._audit_changes = {}

def audit_save(sender, instance, created, **kwargs):
    user = get_current_user()
    ip = get_current_ip()
    action = AuditLog.ACTION_CREATE if created else AuditLog.ACTION_UPDATE
    
    changes = getattr(instance, '_audit_changes', {})
    
    # For creation, we might want to log all initial values
    if created:
        changes = {k: {'old': None, 'new': str(v)} for k, v in model_to_dict(instance).items()}

    AuditLog.objects.create(
        actor=user if user and user.is_authenticated else None,
        ip_address=ip,
        action=action,
        content_type=ContentType.objects.get_for_model(sender),
        object_id=str(instance.pk),
        changes=changes,
        description=f"{sender._meta.verbose_name} {action}d: {str(instance)}"
    )

def audit_delete(sender, instance, **kwargs):
    user = get_current_user()
    ip = get_current_ip()
    
    AuditLog.objects.create(
        actor=user if user and user.is_authenticated else None,
        ip_address=ip,
        action=AuditLog.ACTION_DELETE,
        content_type=ContentType.objects.get_for_model(sender),
        object_id=str(instance.pk),
        description=f"{sender._meta.verbose_name} deleted: {str(instance)}"
    )

def connect_audit_signals():
    # Connect signals dynamically
    for model_path in TRACKED_MODELS:
        try:
            model = apps.get_model(model_path)
            pre_save.connect(audit_pre_save, sender=model, dispatch_uid=f"audit_pre_save_{model_path}")
            post_save.connect(audit_save, sender=model, dispatch_uid=f"audit_save_{model_path}")
            post_delete.connect(audit_delete, sender=model, dispatch_uid=f"audit_delete_{model_path}")
            # print(f"Audit signals connected for {model_path}")
        except (LookupError, ValueError) as e:
            print(f"Failed to connect audit signals for {model_path}: {e}")

connect_audit_signals()


@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR') if request else None
    AuditLog.objects.create(
        actor=user,
        ip_address=ip,
        action=AuditLog.ACTION_LOGIN,
        description="User logged in"
    )

@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR') if request else None
    AuditLog.objects.create(
        actor=user,
        ip_address=ip,
        action=AuditLog.ACTION_LOGOUT,
        description="User logged out"
    )

@receiver(user_login_failed)
def log_login_failed(sender, credentials, request, **kwargs):
    ip = request.META.get('REMOTE_ADDR') if request else None
    AuditLog.objects.create(
        ip_address=ip,
        action=AuditLog.ACTION_LOGIN_FAILED,
        description=f"Login failed for: {credentials.get('username')}"
    )