from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

from django_lifecycle import LifecycleModel, hook, AFTER_SAVE, AFTER_DELETE

from pyhub_ai.models import Conversation
from pyhub_ai.specs import LLMModel


class ChatRoom(LifecycleModel):
    conversation = models.ForeignKey(Conversation, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    llm_model = models.CharField(
        max_length=50,
        choices=[(model.name, model.name) for model in LLMModel],
        default=LLMModel.OPENAI_GPT_4O.value,
    )
    llm_temperature = models.FloatField(
        default=1, validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    llm_system_prompt_template = models.TextField(
        default="""
You are a language tutor.
[언어]로 대화를 나눕시다. 번역과 발음을 제공하지 않고 [언어]로만 답변해주세요.
"[상황]"의 상황으로 상황극을 진행합니다.
가능한한 [언어] [레벨]에 맞는 단어와 표현을 사용해주세요.
--
[언어] : 영어
[상황] : 스타벅스에서 커피 주문
[레벨] : 초급
    """.strip()
    )
    llm_first_user_message_template = models.TextField(
        default="첫 문장으로 대화를 시작하세요."
    )

    def get_absolute_url(self) -> str:
        return reverse("example:situation-chat-room", args=[self.pk])

    @hook(AFTER_SAVE)
    def on_after_save(self):
        if self.conversation is None:
            conv = Conversation.objects.create(user=self.user)
            self.conversation = conv
            self.save(update_fields=["conversation"])

    @hook(AFTER_DELETE)
    def on_after_delete(self):
        if self.conversation:
            self.conversation.delete()

    class Meta:
        ordering = ("-pk",)
