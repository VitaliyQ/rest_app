from rest_framework import permissions


class IsAuthenticateAndNotStaff(permissions.BasePermission):
	def has_permission(self, request, view):
		return bool(request.user.is_authenticated and not request.user.is_staff)
