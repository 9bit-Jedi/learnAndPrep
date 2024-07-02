from django.urls import path
from accounts.views import SendPasswordResetEmailView, UserChangePasswordView, UserLoginView, UserLogoutView, UserProfileView, UserRegestrationView , UserPasswordResetView , StudentClassSelectionView, UserUnregisterView, VerifyOTPView 
from .views import WebsiteUserRegestrationView, OTPVerificationView, MobileNoOTPSendView, MobileNoOTPVerificationView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('register/', UserRegestrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('profile/', UserProfileView.as_view(), name='profile'),
    # path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('select-class/', StudentClassSelectionView.as_view(), name='select class'),
    # path('unregister/', UserUnregisterView.as_view(), name='user-unregister'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),

    # path('verify-email/<uidb64>/<token>/', EmailVerificationView.as_view(), name='verify-email'),
    
    path('website-register/', WebsiteUserRegestrationView.as_view(), name='website-user-register'),
    path('website-verify-otp/', OTPVerificationView.as_view(), name='website-verify-otp'),

    path('mobile-otp/', MobileNoOTPSendView.as_view(), name='send otp to whatsapp for mobile no verification'),
    path('mobile-verify-otp/', MobileNoOTPVerificationView.as_view(), name='verify mobile otp'),
]