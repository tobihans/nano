from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.shortcuts import redirect, render
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import LoginForm, SignupForm
from .models import User
from .tokens import email_verification_token


def signup_view(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            _send_verification_email(request, user)
            messages.success(request, "Check your email to verify your account.")
            return redirect("auth:login")
    else:
        form = SignupForm()
    return render(request, "auth/signup.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.GET.get("next", settings.LOGIN_REDIRECT_URL)
            return redirect(next_url)
    else:
        form = LoginForm()
    return render(request, "auth/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)


def verify_email_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and email_verification_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Email verified. You can now log in.")
    else:
        messages.error(request, "Invalid or expired verification link.")
    return redirect("auth:login")


def _send_verification_email(request, user):
    from django.core.mail import send_mail
    from django.template.loader import render_to_string

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = email_verification_token.make_token(user)
    protocol = "https" if request.is_secure() else "http"
    domain = request.get_host()
    verify_url = f"{protocol}://{domain}/auth/verify-email/{uid}/{token}/"

    subject = "Verify your email"
    html_message = render_to_string(
        "emails/verify_email.html",
        {"user": user, "verify_url": verify_url, "site_name": "Nano"},
    )
    send_mail(
        subject,
        f"Verify your email: {verify_url}",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
    )


# Password reset views using Django's built-in CBVs
class CustomPasswordResetView(PasswordResetView):
    template_name = "auth/password_reset.html"
    email_template_name = "emails/password_reset.txt"
    html_email_template_name = "emails/password_reset.html"
    success_url = "/auth/password-reset/done/"


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "auth/password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "auth/password_reset_confirm.html"
    success_url = "/auth/password-reset/complete/"


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "auth/password_reset_complete.html"
