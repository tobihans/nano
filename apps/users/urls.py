from django.urls import path

from . import views

app_name = "auth"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("verify-email/<uidb64>/<token>/", views.verify_email_view, name="verify-email"),
    path("password-reset/", views.password_reset_view, name="password-reset"),
    path("password-reset/done/", views.password_reset_done_view, name="password-reset-done"),
    path("password-reset/<uidb64>/<token>/", views.password_reset_confirm_view, name="password-reset-confirm"),
    path("password-reset/complete/", views.password_reset_complete_view, name="password-reset-complete"),
]
