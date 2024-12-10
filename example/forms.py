from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Field, Layout, Row
from django import forms

from .layout import JustOneClickableSubmit
from .models import ChatRoom


class ChatRoomForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = [
            "name",
            "llm_model",
            "llm_temperature",
            "llm_system_prompt_template",
            "llm_first_user_message_template",
        ]

    helper = FormHelper()
    helper.attrs = {"novalidate": True}
    helper.layout = Layout(
        "name",
        Row(
            Field("llm_model", wrapper_class="w-1/2"),
            Field("llm_temperature", wrapper_class="w-1/2"),
            css_class="flex gap-2 justify-begin w-full",
        ),
        "llm_system_prompt_template",
        "llm_first_user_message_template",
        ButtonHolder(
            JustOneClickableSubmit(
                css_class="bg-blue-500 hover:bg-blue-700",
                value="저장하기",
            ),
            css_class="flex gap-2 justify-begin",
        ),
    )


class ChatRoomDeleteConfirmForm(forms.Form):
    helper = FormHelper()
    helper.attrs = {"novalidate": True}
    helper.layout = Layout(
        ButtonHolder(
            JustOneClickableSubmit(
                css_class="bg-red-500 hover:bg-red-700",
                value="삭제하겠습니다.",
            ),
            css_class="flex gap-2 justify-begin",
        ),
    )
