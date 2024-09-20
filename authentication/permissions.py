from rest_framework.permissions import BasePermission


class CustomModelPermissions(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Get the action being performed (e.g., 'view', 'change', 'delete')
        if request.method == 'DELETE':
            action = 'destroy'
        else:
            action = view.action

        # Map the action to the corresponding permission codename
        permission_map = {
            'list': 'view_',
            'retrieve': 'view_',
            'export': 'add_',
            'create': 'add_',
            'update': 'change_',
            'partial_update': 'change_',
            'destroy': 'delete_',
            'transfer': 'change_',
        }

        # Determine the required permission
        model = view.queryset.model
        app_label = model._meta.app_label
        model_name = model._meta.model_name
        required_permission = permission_map.get(action) + model_name

        # Check if the user has the required permission
        return request.user.funcao.permissions.filter(codename=required_permission).exists()
