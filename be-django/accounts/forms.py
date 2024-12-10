from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from example.layout import JustOneClickableSubmit
from .models import User


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    helper = FormHelper()
    helper.attrs = {"novalidate": True}
    helper.layout = Layout(
        "username",
        "password1",
        "password2",
        ButtonHolder(
            JustOneClickableSubmit(
                css_class="bg-blue-500 hover:bg-blue-700",
                value="회원가입",
            ),
            css_class="flex gap-2 justify-begin",
        ),
    )


class LoginForm(AuthenticationForm):

    helper = FormHelper()
    helper.attrs = {"novalidate": True}
    helper.layout = Layout(
        "username",
        "password",
        ButtonHolder(
            JustOneClickableSubmit(
                css_class="bg-blue-500 hover:bg-blue-700",
                value="로그인",
            ),
            css_class="flex gap-2 justify-begin",
        ),
    )
