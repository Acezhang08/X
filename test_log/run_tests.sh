#!/bin/bash
# Runs each question 3 times with `claude -p`, each a separate fresh session.
# Runs from an empty directory so no project files/context leak in.
set -u
LOG="$(cd "$(dirname "$0")" && pwd)"
WORK="$(mktemp -d)"
cd "$WORK"
while IFS= read -r line <&3; do
  id="${line%%:*}"; q="${line#*: }"
  for r in 1 2 3; do
    out="$LOG/${id}_run${r}.txt"
    {
      echo "# command: claude -p \"$q\""
      echo "# started: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
      echo "# ---- raw output below ----"
      claude -p "$q" < /dev/null 2>&1
    } > "$out" &
  done
done 3< "$LOG/questions.txt"
wait
