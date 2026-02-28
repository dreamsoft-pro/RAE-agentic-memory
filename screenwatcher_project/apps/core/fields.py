import json
from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.translation import gettext_lazy as _

class LegacyJSONField(models.TextField):
    """
    A JSONField that stores data as a JSON serialized string in a TextField (LONGTEXT).
    Useful for databases that do not support native JSON types (e.g., MariaDB < 10.2).
    """
    description = _("JSON data")

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, (dict, list)):
            return value
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value

    def get_prep_value(self, value):
        if value is None:
            return value
        return json.dumps(value, cls=DjangoJSONEncoder)
