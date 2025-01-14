# Generated by Django 5.1.4 on 2024-12-09 16:26

import django.core.validators
import django.db.models.deletion
import django_lifecycle.mixins
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("pyhub_ai", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ChatRoom",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "llm_model",
                    models.CharField(
                        choices=[
                            ("OPENAI_GPT_4O", "OPENAI_GPT_4O"),
                            ("OPENAI_GPT_4O_MINI", "OPENAI_GPT_4O_MINI"),
                            ("OPENAI_GPT_4_TURBO", "OPENAI_GPT_4_TURBO"),
                        ],
                        default="gpt-4o",
                        max_length=50,
                    ),
                ),
                (
                    "llm_temperature",
                    models.FloatField(
                        default=1,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(1),
                        ],
                    ),
                ),
                (
                    "llm_system_prompt_template",
                    models.TextField(
                        default='You are a language tutor.\n[언어]로 대화를 나눕시다. 번역과 발음을 제공하지 않고 [언어]로만 답변해주세요.\n"[상황]"의 상황으로 상황극을 진행합니다.\n가능한한 [언어] [레벨]에 맞는 단어와 표현을 사용해주세요.\n--\n[언어] : 영어\n[상황] : 스타벅스에서 커피 주문\n[레벨] : 초급'
                    ),
                ),
                (
                    "llm_first_user_message_template",
                    models.TextField(default="첫 문장으로 대화를 시작하세요."),
                ),
                (
                    "conversation",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="pyhub_ai.conversation",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("-pk",),
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
    ]
