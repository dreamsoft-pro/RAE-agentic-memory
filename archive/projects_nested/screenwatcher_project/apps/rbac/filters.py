from rest_framework import filters
from .services import EnforcerService

class CasbinFilterBackend(filters.BaseFilterBackend):
    """
    Filter queryset based on Casbin allowed objects.
    Supports filtering by direct object ID or by related 'machine' ID.
    """
    def filter_queryset(self, request, queryset, view):
        if request.user.is_superuser:
            return queryset

        sub = request.user.username
        act = 'read'
        
        allowed_objs = EnforcerService.get_allowed_objects(sub, act)
        
        # 1. Check for global model permission
        model_label = queryset.model._meta.label_lower
        if model_label in allowed_objs:
            return queryset

        # 2. Extract allowed IDs from Casbin (handles formats: 'machine_1', '1', 'registry.machine_1')
        allowed_ids_per_model = {}
        for obj_str in allowed_objs:
            if '_' in obj_str:
                parts = obj_str.split('_')
                m_name = parts[0].split('.')[-1] # machine or registry.machine -> machine
                m_id = parts[1]
                if m_name not in allowed_ids_per_model:
                    allowed_ids_per_model[m_name] = []
                allowed_ids_per_model[m_name].append(m_id)
            elif obj_str.isdigit():
                # Legacy / simple ID - assume it applies to current model if no other info
                m_name = queryset.model._meta.model_name
                if m_name not in allowed_ids_per_model:
                    allowed_ids_per_model[m_name] = []
                allowed_ids_per_model[m_name].append(obj_str)

        # 3. Apply filtering
        model_name = queryset.model._meta.model_name
        
        # Direct filter for the model itself
        if model_name in allowed_ids_per_model:
            return queryset.filter(pk__in=allowed_ids_per_model[model_name])
        
        # Indirect filter: if this model has a 'machine' field, filter by machine permissions
        if hasattr(queryset.model, 'machine') and 'machine' in allowed_ids_per_model:
            return queryset.filter(machine_id__in=allowed_ids_per_model['machine'])

        # If no permissions found, return empty queryset for safety (Least Privilege)
        return queryset.none()