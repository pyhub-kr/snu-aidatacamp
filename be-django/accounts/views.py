from django import __version__
from django.conf import settings
from django.contrib.auth import login as auth_login, views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import RedirectURLMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.version import get_version_tuple
from django.views.generic import CreateView

from accounts.forms import SignupForm, LoginForm

login = auth_views.LoginView.as_view(
    form_class=LoginForm,
    template_name="form.html",
    redirect_authenticated_user=True,
    success_url_allowed_hosts=settings.SUCCESS_URL_ALLOWED_HOSTS,
)


class LogoutView(auth_views.LogoutView):
    # 장고 5.0에서 제거된 GET 요청에 의한 로그아웃 지원 (비추천)
    if get_version_tuple(__version__) >= (5, 0, 0):
        http_method_names = ["get"] + list(auth_views.LogoutView.http_method_names)

        def get(self, request, *args, **kwargs):
            return self.post(request, *args, **kwargs)


logout = LogoutView.as_view(
    next_page="accounts:login",
    success_url_allowed_hosts=settings.SUCCESS_URL_ALLOWED_HOSTS,
)


class SignupView(RedirectURLMixin, CreateView):
    form_class = SignupForm
    template_name = "form.html"
    # RedirectURLMixin 에서는 성공 이동 주소로서 ?next 인자를 활용하며, 디폴트 주소로서 next_page 설정을 활용
    next_page = "accounts:login"
    success_url_allowed_hosts = settings.SUCCESS_URL_ALLOWED_HOSTS

    def form_valid(self, form):
        response = super().form_valid(form)

        # 자동 로그인
        user = self.object
        auth_login(self.request, user)

        return response


signup = SignupView.as_view()


@login_required
def profile(request):
    return render(request, "accounts/profile.html")


def profile_json(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {
                "is_authenticated": False,
            },
            status=401,
        )
    return JsonResponse(
        {
            "username": request.user.username,
            "is_authenticated": request.user.is_authenticated,
        }
    )
