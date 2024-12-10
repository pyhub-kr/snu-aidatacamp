from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import SignupForm, LoginForm


login = auth_views.LoginView.as_view(
    form_class=LoginForm,
    template_name="form.html",
    redirect_authenticated_user=True,
)


logout = auth_views.LogoutView.as_view(
    next_page="accounts:login",
)


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "form.html"
    success_url = reverse_lazy("accounts:login")


signup = SignupView.as_view()


@login_required
def profile(request):
    return render(request, "accounts/profile.html")
