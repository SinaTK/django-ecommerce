from django.urls import path
from accounts import views

app_name = "accounts"
urlpatterns = [
    path('register/', views.UserRegisterationView.as_view(), name='user_register'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('register-verify/', views.UserRegisterationVirifyCodeView.as_view(), name='register_verify_code'),
    path('register-resend/', views.RegisterResendCodeView.as_view(), name='register_resend_code'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('login-verify/', views.UserLoginVerifyCodeView.as_view(), name= 'login_verify_code'),
    path('logn-resend/', views.LoginResendCodeView.as_view(), name='login_resend_code')
]

