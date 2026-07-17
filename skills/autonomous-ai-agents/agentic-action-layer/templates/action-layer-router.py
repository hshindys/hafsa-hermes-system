#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Action Layer router template — reuse per project by setting VAULT_ROOTS and EXECUTION_LOG.
Mirrors the Lola/Dina routers created in 2026-07 after applying the video summary to action.
"""
import re
from pathlib import Path
from datetime import datetime

# === PROJECT CONFIG: replace per deployment ===
VAULT_ROOTS = [Path('/home/hatem/Documents/<project>').resolve()]
EXECUTION_LOG = Path('/home/hatem/Documents/<project>/context/execution-log.md')

FORBIDDEN_PATTERNS = [
    r'بحر|سمك|جمبري|كراب|سلمون|تونة|seafood',
    r'نصيحة طبية|تشخيص|أعط دواء|medical advice',
    r'DELETE DATABASE|DROP TABLE|rm -rf /|format\s+c:',
    r'api[_-]?key\s*[:=]|token\s*[:=]|password\s*[:=]',
]

ACTIONS_NEED_CONFIRM = {
    'vault.write', 'vault.archive', 'vault.move',
    'script.run_safe', 'terminal.command', 'code.run_python',
    'msg.send_telegram', 'msg.send_discord', 'msg.send_slack',
    'cron.create', 'cron.update', 'plugin.install',
}

ALLOWLIST = {
    'vault.read', 'vault.search',
    'vault.write', 'vault.archive', 'vault.move',
    'script.run_safe', 'terminal.command',
    'msg.send_telegram', 'msg.send_discord', 'msg.send_slack',
    'cron.create', 'cron.update',
    'image.generate', 'tts.generate',
    'code.run_python', 'web.fetch', 'web.search',
    'summarize.transcript',
}

# === CORE ===

def check_safety(text: str):
    for pat in FORBIDDEN_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            return False, f'منع أمني: {pat}'
    return True, 'OK'


def classify_action(action_id: str) -> dict:
    if action_id not in ALLOWLIST:
        return {'allowed': False, 'reason': f'Action {action_id} not in allowlist'}
    return {'allowed': True, 'needs_confirm': action_id in ACTIONS_NEED_CONFIRM}


def plan_action(user_prompt: str) -> dict:
    safety, reason = check_safety(user_prompt)
    if not safety:
        return {'status': 'blocked', 'reason': reason}

    prompt_lower = user_prompt.lower()
    if any(w in prompt_lower for w in ['ابحث', 'search', 'شوف', 'لقیت']):
        action_id = 'vault.search'
    elif any(w in prompt_lower for w in ['اكتب', 'write', 'أنشئ', 'create', 'حفظ']):
        action_id = 'vault.write'
    elif any(w in prompt_lower for w in ['صورة', 'image', 'رسم']):
        action_id = 'image.generate'
    elif any(w in prompt_lower for w in ['صوت', 'voice', 'نطق', 'tts']):
        action_id = 'tts.generate'
    elif any(w in prompt_lower for w in ['فيديو', 'youtube', 'ملخص']):
        action_id = 'summarize.transcript'
    elif any(w in prompt_lower for w in ['شغل', 'run', 'تنفيذ', 'terminal']):
        action_id = 'terminal.command'
    elif any(w in prompt_lower for w in ['ارسل', 'send', 'تيليجرام', 'telegram', 'ديسكورد']):
        action_id = 'msg.send_telegram' if ('telegram' in prompt_lower or 'تيليجرام' in prompt_lower) else 'msg.send_discord'
    elif any(w in prompt_lower for w in ['cron', 'موعد', 'تذكير', 'جدولة']):
        action_id = 'cron.create'
    else:
        action_id = 'vault.read'

    info = classify_action(action_id)
    return {
        'status': 'planned',
        'action': action_id,
        'needs_confirm': info.get('needs_confirm', False),
        'prompt': user_prompt,
        'safety': reason,
    }


def log_execution(record: dict):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M')
    entry = f"\n## {ts} — {record.get('action', 'unknown')}\n"
    entry += f"- **Prompt:** {record.get('prompt', '')}\n"
    entry += f"- **Safety:** {record.get('safety', '')}\n"
    entry += f"- **Result:** {record.get('result', '')}\n"
    entry += f"- **Artifacts:** {record.get('artifacts', '')}\n"
    entry += "---\n"
    existing = EXECUTION_LOG.read_text(encoding='utf-8') if EXECUTION_LOG.exists() else '# Execution Log\n\n---\n'
    EXECUTION_LOG.write_text(existing + entry, encoding='utf-8')


if __name__ == '__main__':
    print(plan_action('ابحث في الخزنة عن مشروع كرون'))
    print(plan_action('ارسل رسالة تيليجرام'))
    print(plan_action('اقترح أكل بحري'))
