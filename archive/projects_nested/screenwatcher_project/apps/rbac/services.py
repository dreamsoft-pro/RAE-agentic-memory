from casbin_adapter.enforcer import enforcer

class EnforcerService:
    @classmethod
    def get_enforcer(cls):
        return enforcer
    
    @classmethod
    def add_policy(cls, sub, obj, act):
        """Adds a permission policy: sub can do act on obj."""
        return enforcer.add_policy(sub, obj, act)
    
    @classmethod
    def add_role_for_user(cls, user, role):
        """Assigns a role to a user."""
        return enforcer.add_grouping_policy(user, role)

    @classmethod
    def enforce(cls, sub, obj, act):
        """Checks permission."""
        return enforcer.enforce(sub, obj, act)

    @classmethod
    def get_allowed_objects(cls, sub, act):
        """
        Returns a list of object identifiers that the subject has permission for.
        Includes permissions inherited from roles.
        Expects policies in format: sub, obj, act
        """
        permissions = enforcer.get_implicit_permissions_for_user(sub)
        # permissions is a list of [sub, obj, act]
        return [p[1] for p in permissions if p[2] == act]
        
    