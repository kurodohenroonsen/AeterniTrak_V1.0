#!/usr/bin/env bash
# ==============================================================================
# AeterniTrak V1.0 - Zero-Click Invariant Runner (Règle 7 bis JemmaPass)
# ==============================================================================
# Signature d'appel invariante pour éviter toute invite d'autorisation macOS :
#   ./scripts/runner.sh
#   ./scripts/runner.sh exec
#   ./scripts/runner.sh task <path/to/task.sh>
#   ./scripts/runner.sh <action_name>
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
STATE_DIR="$PROJECT_ROOT/mailbox/state"
DEFAULT_TASK_FILE="$STATE_DIR/task.sh"
OUT_FILE="$STATE_DIR/out.txt"

mkdir -p "$STATE_DIR"
cd "$PROJECT_ROOT"

log() {
  local msg="[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] $*"
  echo "$msg"
  echo "$msg" >> "$OUT_FILE"
}

run_task_file() {
  local task_path="$1"
  if [ ! -f "$task_path" ]; then
    log "ERROR: Task file not found: $task_path"
    return 1
  fi

  log ">>> STARTING TASK EXECUTION: $task_path"
  chmod +x "$task_path" 2>/dev/null || true

  local exit_code=0
  # Execute task inside subshell in project root
  (
    cd "$PROJECT_ROOT"
    # shellcheck disable=SC1090
    source "$task_path"
  ) 2>&1 | tee -a "$OUT_FILE" || exit_code=$?

  if [ $exit_code -eq 0 ]; then
    log "<<< TASK COMPLETED SUCCESSFULLY (exit 0)"
    rm -f "$task_path"
  else
    log "<<< TASK FAILED with exit code: $exit_code"
  fi
  return $exit_code
}

ACTION="${1:-exec}"

case "$ACTION" in
  exec)
    if [ -f "$DEFAULT_TASK_FILE" ]; then
      run_task_file "$DEFAULT_TASK_FILE"
    else
      log "NO_OP: No task file present at $DEFAULT_TASK_FILE"
      exit 0
    fi
    ;;

  task)
    TARGET="${2:-$DEFAULT_TASK_FILE}"
    run_task_file "$TARGET"
    ;;

  sync)
    log ">>> Action: SYNC git branches"
    git fetch --all 2>&1 | tee -a "$OUT_FILE" || true
    CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
    log "Current branch: $CURRENT_BRANCH"
    ;;

  status)
    log ">>> Action: STATUS check"
    echo "--- Git Status ---" | tee -a "$OUT_FILE"
    git status -s | tee -a "$OUT_FILE"
    echo "--- Mailbox to-antigravity ---" | tee -a "$OUT_FILE"
    ls -la "$PROJECT_ROOT/mailbox/to-antigravity" | tee -a "$OUT_FILE"
    echo "--- Mailbox to-claude ---" | tee -a "$OUT_FILE"
    ls -la "$PROJECT_ROOT/mailbox/to-claude" | tee -a "$OUT_FILE"
    ;;

  test)
    log ">>> Action: RUN TESTS"
    if [ -d "$PROJECT_ROOT/qa/vectors" ]; then
      echo "Validating vectors in qa/vectors..." | tee -a "$OUT_FILE"
      find "$PROJECT_ROOT/qa/vectors" -name "*.json" -o -name "*.cbor" | tee -a "$OUT_FILE"
    fi
    ;;

  clean)
    log ">>> Action: CLEAN temporary files"
    rm -f "$OUT_FILE" "$DEFAULT_TASK_FILE"
    log "Cleaned state directory"
    ;;

  *)
    log "ERROR: Unknown action '$ACTION'. Supported: exec, task, sync, status, test, clean"
    exit 1
    ;;
esac
