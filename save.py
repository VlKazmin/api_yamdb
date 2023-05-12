class IsAdmin(permissions.BasePermission):
+    def has_permission(self, request, view):
+        return request.user.is_authenticated and request.user.is_admin
+
+
+class ReadOnly(permissions.BasePermission):
+    def has_permission(self, request, view):
+        return request.method in permissions.SAFE_METHODS



