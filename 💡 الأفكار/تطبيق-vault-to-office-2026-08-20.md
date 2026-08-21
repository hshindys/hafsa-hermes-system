---
type: report
title: 📊 vault_to_office — تصدير التقارير الطبية لـ XLSX/PDF (2026-08-20)
tags: [vault-to-office, export, xlsx, pdf, medical, gemini-notebook-style]
---
# 📊 vault_to_office — تصدير التقارير الطبية لـ Office

## ✅ اللي اتعمل:
- ✅ `vault_to_office.py` — بيقرأ مجلد `💊 طبي` ويصدّر الجداول لـ Office
- ✅ **XLSX** (Excel): `medical_reports.xlsx` (2 tables، منظّم بألوان هفصة 💕)
- ✅ **PDF**: `medical_reports.pdf` (جداول منظّمة)
- يمثّل ميزة Gemini Notebook (تصدير Word/Excel/PPT) بس **على ستاكنا المحلي**

## 💡 طريقة التشغيل:
```bash
cd C:/Users/hshin/AppData/Local/Temp/voicetest
uv run --with openpyxl python "C:/Users/hshin/AppData/Local/hermes/shared_memory/vault_to_office.py" xlsx
uv run --with reportlab python "C:/Users/hshin/AppData/Local/hermes/shared_memory/vault_to_office.py" pdf
# أو all لكن لازم كل واحد لوحده (Device Guard)
```

## 📌 الفائدة:
- تصدير الخطة اليومية/المتابعة لـ Excel (يسهّل على الدكتور يقرأها)
- PDF رسمي للطباعة
- كله **local + offline** (مفيش cloud، مفيش تسريب أسرار طبية)

## ⚠️ ملاحظة Device Guard:
- `uv run --with openpyxl reportlab` مع بعض بيفشل (Application Control blocks)
- الحل: كل مكتبة لوحدها (`--with openpyxl` ثم `--with reportlab`)

## 🔗 الملفات:
- `C:\Users\hshin\AppData\Local\hermes\shared_memory\vault_to_office.py`
- `D:\vaults\Hafsa\medical_reports.xlsx` / `.pdf`
