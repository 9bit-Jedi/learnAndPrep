from django.urls import path
from accounts.views import SendPasswordResetEmailView, UserChangePasswordView, UserLoginView, UserProfileView, UserRegestrationView , UserPasswordResetView , StudentClassSelectionView, UserUnregisterView, VerifyOTPView 
from .views import WebsiteUserRegestrationView, OTPVerificationView

urlpatterns = [
    path('register/', UserRegestrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    # path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('select-class/', StudentClassSelectionView.as_view(), name='select class'),
    path('unregister/', UserUnregisterView.as_view(), name='user-unregister'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    
    path('website-register/', WebsiteUserRegestrationView.as_view(), name='website-user-register'),
    path('website-verify-otp/', OTPVerificationView.as_view(), name='website-verify-otp'),
]

    # path('verify-email/<uidb64>/<token>/', EmailVerificationView.as_view(), name='verify-email'),