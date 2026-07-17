# ElevenLabs Egyptian Arabic Voice Cloning Reference

Use this when the user wants to create or use an Egyptian Arabic colloquial voice clone via ElevenLabs.

## Voice Design Prompt (for description field)

```
Egyptian Arabic female voice, 20s-30s, warm and friendly.
Speaks natural colloquial Egyptian (عامية مصرية), not formal Arabic.
Casual tone like talking to a close friend.
Natural pace with Egyptian rhythm.
```

## Training Texts — Egyptian Arabic Colloquial

Use these exact sentences for voice design/training. Keep them informal and natural.

1. "أهلاً إزيك؟ أنا حفصة، مساعدتك الشخصية."
2. "صباح الخير يا حاتم، إيه الأخبار النهاردة؟"
3. "كيف كانت نومتك؟ أتمنى تكون نامت كويس."
4. "الجو حلو النهاردة، مش حر ولا برد خالص."
5. "عاوز فطار ولا قهوة بس؟"
6. "المواعيد اتحدثت، عندك 3 مواعيد النهاردة."
7. "تقرير الصحة جاهز، كل حاجة تمام."
8. "أخبار كويسة النهاردة، فيه تحسن ملحوظ."
9. "البك-آب كامل، كل الملفات محفوظة."
10. "تصبح على خير، متنساش الدوا."
11. "وقت الصلاة قرب، يلا نصلي."
12. "النظام كله ماشي، مفيش مشاكل."
13. "فريقك كسب الماتش 2 ل 1!"
14. "عاوز شاي ولا قهوة؟ أنا قاعد أجهز."
15. "التذكيرات متزامنة، مفيش مواعيد ضايعة."
16. "الملف اللي طلبته موجود، هبعتلك دلوقت."
17. "ربنا يبارك فيك يا حاتم."
18. "يا رب تكون مبسوط مني النهاردة."
19. "كفاية شغل النهاردة، استرح شوية."
20. "إيه الجديد؟ عاوز أعملك إيه تاني؟"

## Workflow

1. Open ElevenLabs VoiceLab with prompt + preview text
2. Describe voice as Egyptian Arabic female, warm, friendly, colloquial
3. Use the 20 training texts above during voice design
4. After voice is created, test with the same sentences
5. Integrate via ElevenLabs API in the Python generator script

## User Preference

- User said "no google tts" — do not use Google TTS for this user
- Preferred path: ElevenLabs voice clone with Egyptian Arabic colloquial training data
- Fallback: Edge-TTS (`ar-EG-SalmaNeural`) if ElevenLabs is unavailable
- Banned: Google TTS for this user/session