class LegacyDatabaseRouter:
    """
    A router to control all database operations on models in the
    legacy_integration application.
    """
    route_app_labels = {'legacy_integration'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            if model._meta.model_name == 'connectionprofile':
                return 'default'
            return 'external_legacy'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            if model._meta.model_name == 'connectionprofile':
                return 'default'
            return 'external_legacy'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        # Allow relations if one of them is ConnectionProfile (which is now in default)
        # and it's linked to Machine (also in default).
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            if model_name == 'connectionprofile':
                return db == 'default'
            return db == 'external_legacy'
        return None
