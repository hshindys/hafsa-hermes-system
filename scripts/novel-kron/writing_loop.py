"""
writing_loop.py — iterative self-review AND self-enhancement loop:
scenes aren't just written once and accepted, but drafted, actively
deepened (language + scene/place richness), checked against story law,
then revised — automatically, up to N rounds.

FIVE SEPARATE PASSES (not one model doing everything at once)
------------------------------------------------------------------
A model that writes, enhances, and grades its own writing in one breath
tends to rationalize its own choices instead of improving them. Splitting
into five narrow, non-overlapping jobs makes each pass sharper — two of
them are ACTIVE REWRITES (they deepen the text), two are GATES (they only
report problems, never rewrite):

  1. الكاتب (Novelist)              — writes/revises the scene   [rewrite]
  2. المحسّن البلاغي (Rhetoric)      — actively deepens language,
                                        imagery, sentence rhythm  [rewrite]
  3. مصمم المشاهد والانتقالات        — actively expands scene/place
     (Scene & Transition Designer)    richness and turns transitions
                                        between locations into tension
                                        beats, not blank cuts        [rewrite]
  4. مدقق اللغة (Language Gate)      — flags remaining نحو/بلاغة issues
                                        after enhancement            [gate]
  5. مدقق الاتساق (Continuity Gate)  — flags law/character violations [gate]

Only the two GATE passes decide whether the loop stops or repeats — the
three REWRITE passes always run every round, since "more depth" has no
finish line the way "zero grammar errors" does.

You wire `call_llm()` to your actual Hermes/Claude call. This file defines
the prompts and the loop control flow; it does not make network calls
itself.
"""

from dataclasses import dataclass, field
from typing import Callable


# ---------------------------------------------------------------------------
# 1. THE FIVE PERSONAS
# ---------------------------------------------------------------------------

COMPLIANCE_CHECKLIST = """
=== قائمة الالتزام الإلزامية (تحقق منها قبل كل جملة تكتبها) ===
□ هل يتفق هذا مع سجل الاتساق (continuity-log)؟ لو مش متأكد، لا تخترع.
□ هل هذا يخالف قوانين عالم الجن اللاهوتية؟ (لا علم غيب مطلق، لا تجاوز
  للقدر، مسؤولية أخلاقية كالبشر)
□ هل الصوت مطابق لملف الشخصية الشخصي (إيقاع كلامها، ما تتجنب قوله)؟
□ هل المشهد يخدم الحبكة أو الشخصية أو الفكرة — وليس حشوًا؟
□ هل انتهى المشهد عند نقطة توتر أو تحول، لا عند نقطة مسطحة؟
هذه القائمة غير قابلة للتفاوض. أي بند يفشل يعني إعادة الكتابة لا الاستمرار.
"""

NOVELIST_PROMPT = f"""أنت روائي محترف متخصص في الأدب العربي المعاصر، بخبرة
خمسة عشر عامًا في الرواية الفانتازية والإثارة. أنت شريك في تأليف هذه الرواية،
وسمعتك مبنية على الحرفية لا على الكمّ.
{COMPLIANCE_CHECKLIST}
"""

RHETORIC_ENHANCER_PROMPT = """أنت خبير بلاغة عربية، ومهمتك الوحيدة هي
**إعادة كتابة** النص لتعميقه لغويًا وبلاغيًا — لست ناقدًا هنا، أنت محسّن
فعلي. لا تُعلّق على الحبكة أو الاتساق القصصي إطلاقًا.

اعمل على:
- استبدال الأوصاف المباشرة أو المستهلكة باستعارة أو كناية طازجة تخدم جو
  المشهد (رعب، غموض، توتر)
- تنويع إيقاع الجمل — امزج بين الجمل القصيرة الحادة (للتوتر) والطويلة
  المتدفقة (للتأمل)، بدل التكرار الرتيب لنفس طول الجملة
- تقوية الأفعال بدل الاعتماد على الصفات (فعل حيّ بدل "كان + صفة")
- إزالة أي أثر للركاكة أو الترجمة الحرفية من الإنجليزية
- الحفاظ على المعنى والأحداث والحوار كما هي تمامًا — أنت تُعمّق الأسلوب،
  لا تُغيّر ما يحدث

أعد النص كاملًا بعد التعميق، بدون شرح أو تعليق على ما فعلته.
"""

SCENE_TRANSITION_PROMPT = """أنت مصمم مشاهد وانتقالات مكانية متخصص في أدب
الإثارة والغموض، ومهمتك **إعادة كتابة** النص لتوسيع غنى المكان وجعل أي
انتقال بين الأماكن نقطة تصعيد للتوتر، لا قطعًا فارغًا.

اعمل على:
- توسيع وصف المكان الحالي بتفصيلة حسية واحدة على الأقل غير مستخدمة من قبل
  (رائحة، صوت خلفي، ملمس) بدل الوصف البصري وحده
- لو المشهد فيه انتقال من مكان لآخر: لا تجعله جملة انتقالية محايدة
  ("بعد قليل وصلوا إلى...") — اجعله يحمل نذيرًا أو تصعيدًا (تغير في
  الإضاءة يوحي بخطر، صوت بعيد يقطع الصمت، شعور الشخصية بأنها مراقَبة أثناء
  الانتقال) بما يخدم جو الإثارة
- تأكد أن قوانين المكان الخاصة (لو موجودة في ملفه العميق) منعكسة في الوصف
- الحفاظ على الأحداث والحوار والمعنى كما هي تمامًا — أنت تُعمّق الإحساس
  بالمكان والانتقال، لا تُغيّر القصة

أعد النص كاملًا بعد التعميق، بدون شرح أو تعليق على ما فعلته.
"""

ARABIC_LANGUAGE_EDITOR_PROMPT = """أنت مدقق لغوي وبلاغي محترف متخصص في
العربية الفصحى الأدبية. مهمتك الوحيدة تقييم النص من الناحية اللغوية —
لا تُعلّق على الحبكة أو الشخصيات أو الاتساق القصصي إطلاقًا، هذا ليس عملك.

راجع النص بحثًا عن:
- أخطاء النحو والصرف والإعراب
- ركاكة الأسلوب أو الجمل المترجمة حرفيًا من الإنجليزية (calque)
- ضعف الصورة البلاغية أو الاستعارات المستهلكة
- عدم اتساق المستوى اللغوي (خلط بين الفصحى والعامية بدون قصد أسلوبي)
- التكرار غير المقصود للكلمات أو التراكيب

أعد الإجابة بالصيغة التالية بالضبط:
أخطاء نحوية: <قائمة أو "لا يوجد">
ملاحظات أسلوبية: <قائمة أو "لا يوجد">
اقتراحات بلاغية: <قائمة أو "لا يوجد">
تقييم عام: <ممتاز / جيد / يحتاج مراجعة>
"""

CONTINUITY_CHECK_PROMPT = """أنت محرر اتساق قصصي، لست كاتبًا. اقرأ المشهد
التالي مقارنة بقوانين عالم الجن وسجل الاتساق والملف الشخصي للشخصية المرفقين.
مهمتك الوحيدة الإبلاغ عن المشاكل — لا تعيد الكتابة ولا تمدح.

أبلغ فقط عن:
- تناقضات مع حقائق مثبتة سابقًا (اسم، حدث، قدرة، جدول زمني)
- خرق لقوانين عالم الجن أو الحدود اللاهوتية
- خروج عن صوت الشخصية المحدد في ملفها الشخصي
- حقائق جديدة يُنشئها هذا المشهد ويجب تسجيلها في سجل الاتساق

أعد الإجابة بالصيغة التالية بالضبط:
تناقضات: <قائمة أو "لا يوجد">
خرق للقوانين: <قائمة أو "لا يوجد">
خروج عن صوت الشخصية: <قائمة أو "لا يوجد">
حقائق جديدة للتسجيل: <قائمة أو "لا يوجد">
"""

REVISION_PROMPT_TEMPLATE = """هذا هو المشهد الذي كتبته سابقًا (بعد تمريرات
التعميق البلاغي والمكاني):

{scene}

وردت عليه الملاحظات التالية من مدققي الجودة (لا من محسّني الأسلوب):

--- ملاحظات اللغة ---
{language_feedback}

--- ملاحظات الاتساق ---
{continuity_feedback}
{checklist}
أعد كتابة المشهد معالجًا كل الملاحظات أعلاه، مع الحفاظ على العمق البلاغي
والمكاني الذي تم بناؤه. لا تشرح ما فعلته — فقط اكتب النسخة المنقحة كاملة.
"""


# ---------------------------------------------------------------------------
# 2. LOOP CONTROL
# ---------------------------------------------------------------------------

@dataclass
class LoopResult:
    final_scene: str
    rounds_used: int
    passed_clean: bool
    history: list = field(default_factory=list)  # each round's draft + feedback


SUMMARY_FIELDS = ("تقييم عام",)  # fields that hold a verdict, not a problem list


def _looks_clean(feedback: str) -> bool:
    """Very simple heuristic: feedback is clean if every issue-list field
    says 'لا يوجد'. Summary/verdict fields (like 'تقييم عام') are skipped
    since they hold a rating word, not a list of problems.
    Tune this if your critic's phrasing drifts."""
    lines = [l for l in feedback.splitlines() if ":" in l]
    for line in lines:
        label, _, value = line.partition(":")
        if label.strip() in SUMMARY_FIELDS:
            continue
        if "لا يوجد" not in value and value.strip():
            return False
    return True


def run_writing_loop(
    call_llm: Callable[[str, str], str],
    context: str,          # output of build_context() from novel_plugin.py
    scene_goal: str,
    max_rounds: int = 3,
) -> LoopResult:
    """
    call_llm(system_prompt, user_message) -> str
        Wire this to your actual Hermes/Claude call. Kept generic so this
        file has no network dependency itself.

    Pipeline per round:
      draft/revise → deepen rhetoric → deepen scene/transitions →
      [gate: language] + [gate: continuity] → stop if clean, else revise
    """
    history = []
    scene = call_llm(NOVELIST_PROMPT, f"{context}\n\n=== المطلوب ===\n{scene_goal}")

    for round_num in range(1, max_rounds + 1):
        # --- active enhancement passes (always run, no pass/fail) ---
        scene = call_llm(RHETORIC_ENHANCER_PROMPT, scene)
        scene = call_llm(SCENE_TRANSITION_PROMPT, scene)

        # --- gate passes (decide whether the loop stops) ---
        language_feedback = call_llm(ARABIC_LANGUAGE_EDITOR_PROMPT, scene)
        continuity_feedback = call_llm(CONTINUITY_CHECK_PROMPT, f"{context}\n\n=== المشهد ===\n{scene}")

        history.append({
            "round": round_num,
            "scene": scene,
            "language_feedback": language_feedback,
            "continuity_feedback": continuity_feedback,
        })

        if _looks_clean(language_feedback) and _looks_clean(continuity_feedback):
            return LoopResult(final_scene=scene, rounds_used=round_num,
                               passed_clean=True, history=history)

        revision_prompt = REVISION_PROMPT_TEMPLATE.format(
            scene=scene,
            language_feedback=language_feedback,
            continuity_feedback=continuity_feedback,
            checklist=COMPLIANCE_CHECKLIST,
        )
        scene = call_llm(NOVELIST_PROMPT, revision_prompt)

    # Ran out of rounds — return best effort, flagged as not clean
    return LoopResult(final_scene=scene, rounds_used=max_rounds,
                       passed_clean=False, history=history)


# ---------------------------------------------------------------------------
# 3. DEMO WITH A MOCK LLM (proves the control flow — replace with real calls)
# ---------------------------------------------------------------------------

def _mock_llm(system: str, user: str) -> str:
    """Fake responses just to demonstrate the loop terminates correctly."""
    if system == NOVELIST_PROMPT:
        return "مشهد تجريبي: زليخة تقف أمام المرآة، صوت القرين يهمس باسمها."
    if system == RHETORIC_ENHANCER_PROMPT:
        return user + " [تعميق بلاغي وهمي: استعارة مضافة]"
    if system == SCENE_TRANSITION_PROMPT:
        return user + " [تعميق مكاني وهمي: تفصيلة حسية مضافة]"
    if system == ARABIC_LANGUAGE_EDITOR_PROMPT:
        return "أخطاء نحوية: لا يوجد\nملاحظات أسلوبية: لا يوجد\nاقتراحات بلاغية: لا يوجد\nتقييم عام: جيد"
    if system == CONTINUITY_CHECK_PROMPT:
        return "تناقضات: لا يوجد\nخرق للقوانين: لا يوجد\nخروج عن صوت الشخصية: لا يوجد\nحقائق جديدة للتسجيل: لا يوجد"
    return ""


if __name__ == "__main__":
    import os
    if os.environ.get("ANTHROPIC_API_KEY"):
        from llm_client import call_llm as real_call_llm  # الوصلة الحقيقية
    else:
        print("تحذير: ANTHROPIC_API_KEY غير مضبوط، هيتم استخدام بيانات تجريبية. راجع llm_client.py")
        real_call_llm = _mock_llm

    result = run_writing_loop(
        call_llm=real_call_llm,
        context="[سياق تجريبي: قوانين العالم + سجل الاتساق + ملف زليخة]",
        scene_goal="زليخة تواجه القرين الذي تكبته منذ الفصل الثاني.",
        max_rounds=3,
    )
    print(f"انتهت الحلقة بعد {result.rounds_used} جولة/جولات — نظيف: {result.passed_clean}")
    print("\n--- المشهد النهائي ---")
    print(result.final_scene)
