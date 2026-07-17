# Al-Ahly Vault — Bootstrap script

Run once to create the folder tree and drop-in files.

```bash
#!/usr/bin/env bash
set -euo pipefail
ROOT="$HOME/Documents/Hatem Nad/01-Projects/Nadi Al-Ahly"
mkdir -p "$ROOT/Matches" "$ROOT/Competitions" "$ROOT/News"
cat > "$ROOT/Overview.md" <<'EOF'
# 📋 Overview — النادي الأهلي المصري
> آخر تحديث: $(date +%Y-%m-%d)
EOF
cat > "$ROOT/Matches/Schedule.md" <<'EOF'
# 📅 جدول المباريات القادمة — النادي الأهلي المصري
> آخر تحديث: $(date +%Y-%m-%d)
EOF
cat > "$ROOT/Matches/Log.md" <<'EOF'
# 📋 سجل المباريات — النادي الأهلي المصري
> آخر تحديث: $(date +%Y-%m-%d)
EOF
cat > "$ROOT/Competitions/Premier-League.md" <<'EOF'
# 🏆 الدوري المصري الممتاز — موسم 2025/2026
> آخر تحديث: $(date +%Y-%m-%d)
EOF
cat > "$ROOT/Competitions/CAF-Champions-League.md" <<'EOF'
# 🏆 دوري أبطال أفريقيا — موسم 2025/2026
> آخر تحديث: $(date +%Y-%m-%d)
EOF
cat > "$ROOT/Competitions/Cup.md" <<'EOF'
# 🏆 كأس مصر / السوبر المصري
> آخر تحديث: $(date +%Y-%m-%d)
EOF
cat > "$ROOT/Squad.md" <<'EOF'
# 👥 تشكيلة الأهلي — موسم 2025/2026
> آخر تحديث: $(date +%Y-%m-%d)
EOF
cat > "$ROOT/News/Clips.md" <<'EOF'
# 🔗 روابط + ملخصات — النادي الأهلي المصري
> آخر تحديث: $(date +%Y-%m-%d)
EOF
echo "Created: $ROOT"
```
