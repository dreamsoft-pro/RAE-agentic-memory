from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Operator(models.Model):
    """
    Production operator profile linking to a system user.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='operator_profile'
    )
    badge_id = models.CharField(_("Badge ID"), max_length=50, unique=True, blank=True, null=True)
    default_machine = models.ForeignKey(
        'registry.Machine',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='default_operators'
    )

    class Meta:
        verbose_name = _("Operator")
        verbose_name_plural = _("Operators")

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.badge_id})"


class ReasonCode(models.Model):
    """
    Standardized codes for stops, pauses, and scraps.
    """
    SEVERITY_INFO = 'INFO'
    SEVERITY_WARNING = 'WARNING'
    SEVERITY_CRITICAL = 'CRITICAL'

    SEVERITY_CHOICES = [
        (SEVERITY_INFO, 'Info'),
        (SEVERITY_WARNING, 'Warning'),
        (SEVERITY_CRITICAL, 'Critical'),
    ]

    code = models.CharField(_("Code"), max_length=50, unique=True)
    description = models.CharField(_("Description"), max_length=255)
    category = models.CharField(_("Category"), max_length=50, blank=True, help_text=_("e.g., Mechanical, Electrical, Operational"))
    severity = models.CharField(_("Severity"), max_length=20, choices=SEVERITY_CHOICES, default=SEVERITY_INFO)

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Reason Code")
        verbose_name_plural = _("Reason Codes")
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.description}"
