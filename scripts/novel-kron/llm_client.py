"""
llm_client.py — الوصلة الحقيقية بـ Claude API. استخدمها بدل _mock_llm في
enrich.py و writing_loop.py.

الإعداد لمرة واحدة
--------------------
1. احصل على مفتاح API من: https://console.anthropic.com/settings/keys
2. صدّره كمتغير بيئة (أضف السطر ده في ~/.bashrc أو ~/.zshrc عندك):
   export ANTHROPIC_API_KEY="sk-ant-..."
3. pip install anthropic --break-system-packages

الاستخدام في أي سكريبت من اللي عملناهم
-----------------------------------------
بدل:
    call_llm = _mock_llm
اكتب:
    from llm_client import call_llm
"""

import os
from anthropic import Anthropic

_client = None


def _get_client() -> Anthropic:
    global _client
    if _client is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "متغير البيئة ANTHROPIC_API_KEY غير موجود. "
                "راجع تعليمات الإعداد في أعلى هذا الملف."
            )
        _client = Anthropic(api_key=api_key)
    return _client


def call_llm(system_prompt: str, user_message: str,
             model: str = "claude-sonnet-4-6", max_tokens: int = 4096) -> str:
    """التوقيع مطابق تمامًا لما تتوقعه enrich.py و writing_loop.py:
    call_llm(system_prompt, user_message) -> str"""
    client = _get_client()
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )
    return "".join(block.text for block in response.content if block.type == "text")


if __name__ == "__main__":
    # اختبار سريع: هيفشل بوضوح لو المفتاح مش موجود، بدل ما يفشل بغموض لاحقًا
    try:
        result = call_llm("أنت مساعد مفيد.", "قول 'الوصلة شغالة' بالعربي فقط.")
        print("نجح الاختبار:", result)
    except EnvironmentError as e:
        print(f"لسه محتاج إعداد: {e}")
