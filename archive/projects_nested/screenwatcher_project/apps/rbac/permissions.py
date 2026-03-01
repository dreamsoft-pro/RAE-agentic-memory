from rest_framework import permissions
from .services import EnforcerService

class CasbinPermission(permissions.BasePermission):
    """
    Grant access based on Casbin RBAC policies.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
            
        # Superuser bypass - GLOBAL OVERRIDE
        if request.user.is_superuser:
            return True
            
        # Get username as subject
        sub = request.user.username
        
        # Determine model-level object name
        if hasattr(view, 'queryset') and view.queryset is not None:
            model_label = view.queryset.model._meta.label_lower # e.g., 'registry.machine'
            model_name = view.queryset.model._meta.model_name
        else:
            model_label = view.__class__.__name__
            model_name = None

        method_map = {
            'GET': 'read',
            'POST': 'write',
            'PUT': 'update',
            'PATCH': 'update',
            'DELETE': 'delete'
        }
        act = method_map.get(request.method, 'read')

        # Check global permission for the model
        if EnforcerService.enforce(sub, model_label, act):
            return True

        # Special Case: for 'read' actions (listing), allow if the user has permission 
        # for ANY specific instance of this model. The FilterBackend will do the actual filtering.
        if act == 'read' and model_name:
            allowed_objs = EnforcerService.get_allowed_objects(sub, act)
            for allowed in allowed_objs:
                if f"{model_name}_" in allowed or allowed.isdigit():
                    return True

        return False

    def has_object_permission(self, request, view, obj):
        """
        Check if user has permission for a specific object instance.
        """
        # Superuser bypass - GLOBAL OVERRIDE
        if request.user.is_superuser:
            return True

        sub = request.user.username
        
        obj_id = f"{obj._meta.model_name}_{obj.pk}"
        
        method_map = {
            'GET': 'read',
            'POST': 'write',
            'PUT': 'update',
            'PATCH': 'update',
            'DELETE': 'delete'
        }
        act = method_map.get(request.method, 'read')
        
        # 1. Check specific object permission (e.g. 'machine_5')
        if EnforcerService.enforce(sub, obj_id, act):
            return True
            
        # 2. Check global model permission (e.g. 'registry.machine')
        model_label = obj._meta.label_lower
        return EnforcerService.enforce(sub, model_label, act)
