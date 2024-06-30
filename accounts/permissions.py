from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from django.shortcuts import get_object_or_404
from .models import User

class IsPaymentDone(BasePermission):
    message = 'User is not enrolled in Mentorship Programme. Payment has to be done successfully to be enrolled.' 
    def has_permission(self, request, view):
        return request.user.has_perm('accounts.is_payment_done')

class IsMentorAlloted(BasePermission):
    message = 'No mentor has been alloted to you.' 
    def has_permission(self, request, view):
        return request.user.has_perm('accounts.is_mentor_alloted')
