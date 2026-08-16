---
type: self-hosted-guide
title: تطبيقات Self-Hosted (Immich + RustDesk + AppFlowy)
tags: [self-hosted, docker, خصوصية, immich, rustdesk, appflowy, vps]
---
# 🐳 تطبيقات Self-Hosted — بدائل مجانية مفتوحة المصدر

> المصدر: فيديو `jMAe1h39rHo` (10 بدائل للتطبيقات المدفوعة).
> الحالة: **الإعداد جاهز** — محتاج VPS (Tencent Cloud free trial / أي Ubuntu) عشان يشتغل.

## التطبيقات (ومن بتستبدل)
| التطبيق | يستبدل | الفائدة لحاتم |
|---------|---------|----------------|
| **Immich** | Google Photos | صورك وألبوم حفصة عندك (خصوصية) |
| **RustDesk** | TeamViewer | تحكم عن بُعد آمن (relay بتاعك) |
| **AppFlowy** | Notion | docs/wikis/Kanban يتحكم فيها (مكمّل للـ Obsidian) |

## ملفات الإعداد
موجودة في `C:\Users\hshin\AppData\Local\hermes\shared_memory\self-hosted\`:
- `immich.yml` · `rustdesk.yml` · `appflowy.yml` (docker-compose)

## خطوات التشغيل على الـ VPS
1. اشترِ/جهّز VPS (Ubuntu 22.04+, docker مثبّت).
2. انسخ ملفات `self-hosted/*.yml` للـ VPS (scp).
3. لكل تطبيق:
   ```
   mkdir -p /opt/<app> && cd /opt/<app>
   # الصق الـ yml هنا
   docker compose up -d
   ```
4. افتح الـ ports: Immich 2283 · RustDesk 21115-21119 · AppFlowy 3000.
5. غيّر كلمات السر (`change_me_*`) قبل ما تنشر.

## ⚠️ ملاحظات أمان
- Immich: التزم بـ 3-2-1 backup (ما فيش Google بتعملها لك).
- RustDesk: الـ relay بتاعك = البيانات ما تعديش على سيرفر تالت.
- كل التطبيقات: غيّر كلمات السر الافتراضية فوراً.

## حالة التنفيذ
- [x] compose files جاهزة
- [ ] VPS موجود (معلّق لحد ما تجيب Tencent Cloud / بديل)
- [ ] تشغيل فعلي (بعد الـ VPS)
