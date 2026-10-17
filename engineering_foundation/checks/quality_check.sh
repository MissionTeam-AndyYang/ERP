#!/usr/bin/env sh
set -u

fail_on_unavailable=0
report_path=''
while [ "$#" -gt 0 ]; do
  case "$1" in
    --fail-on-unavailable) fail_on_unavailable=1 ;;
    --report-path) shift; report_path="${1:-}" ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
  shift
done

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
pass_count=0
fail_count=0
unavailable_count=0
results=''

record() {
  name=$1
  status=$2
  command_text=$3
  detail=$4
  results="${results}${name}|${status}|${command_text}|${detail}\n"
  case "$status" in
    PASS) pass_count=$((pass_count + 1)) ;;
    FAIL) fail_count=$((fail_count + 1)) ;;
    UNAVAILABLE) unavailable_count=$((unavailable_count + 1)) ;;
  esac
}

run_check() {
  name=$1
  command_text=$2
  shift 2
  if "$@" >/tmp/cf02_quality_check.out 2>&1; then
    record "$name" PASS "$command_text" 'Completed successfully.'
  else
    code=$?
    cat /tmp/cf02_quality_check.out
    record "$name" FAIL "$command_text" "Exited with code $code."
  fi
}

cd "$repo_root" || exit 1
if command -v git >/dev/null 2>&1; then
  run_check git-diff-check 'git diff --check -- .' git diff --check -- .
else
  record git-diff-check UNAVAILABLE 'git diff --check -- .' 'Git executable not found.'
fi

if ! command -v npm >/dev/null 2>&1; then
  record frontend-lint UNAVAILABLE 'npm run lint' 'npm not found; no runtime substitution attempted.'
  record frontend-build UNAVAILABLE 'npm run build' 'npm not found; no runtime substitution attempted.'
elif [ ! -d "$repo_root/node_modules" ]; then
  record frontend-lint UNAVAILABLE 'npm run lint' 'node_modules is absent; npm ci was not run by this check.'
  record frontend-build UNAVAILABLE 'npm run build' 'node_modules is absent; npm ci was not run by this check.'
else
  run_check frontend-lint 'npm run lint' npm run lint
  run_check frontend-build 'npm run build' npm run build
fi

backend_python="$repo_root/backend/.venv/bin/python"
if [ ! -x "$backend_python" ]; then
  record backend-ruff UNAVAILABLE 'backend/.venv/bin/python -m ruff check app tests alembic' 'backend/.venv is absent; global Python was not used.'
  record backend-pytest UNAVAILABLE 'backend/.venv/bin/python -m pytest -p no:cacheprovider' 'backend/.venv is absent; global Python was not used.'
else
  cd "$repo_root/backend" || exit 1
  run_check backend-ruff 'backend/.venv/bin/python -m ruff check app tests alembic' "$backend_python" -m ruff check app tests alembic
  run_check backend-pytest 'backend/.venv/bin/python -m pytest -p no:cacheprovider' "$backend_python" -m pytest -p no:cacheprovider
fi

printf 'Summary: PASS=%s FAIL=%s UNAVAILABLE=%s\n' "$pass_count" "$fail_count" "$unavailable_count"
printf '%b' "$results"

if [ -n "$report_path" ]; then
  report_file="$report_path"
  case "$report_file" in
    /*) ;;
    *) report_file="$repo_root/$report_file" ;;
  esac
  report_dir=$(dirname -- "$report_file")
  mkdir -p "$report_dir"
  {
    printf '# CF-02 Offline Verification Report\n\n'
    printf 'Generated: %s\n' "$(date -Iseconds)"
    printf 'Scope: isolated static/offline checks for this FM02 repository checkout.\n\n'
    printf '| Check | Status | Command | Detail |\n| --- | --- | --- | --- |\n'
    printf '%b' "$results" | while IFS='|' read -r name status command_text detail; do
      [ -n "$name" ] && printf '| %s | %s | `%s` | %s |\n' "$name" "$status" "$command_text" "$detail"
    done
    printf '\nSummary: PASS=%s; FAIL=%s; UNAVAILABLE=%s.\n\n' "$pass_count" "$fail_count" "$unavailable_count"
    printf 'No dependency installation, global runtime change, database/migration execution, application-code edit, or evidence rewrite is performed by this entry point.\n'
  } > "$report_file"
  printf 'Report written: %s\n' "$report_file"
fi

if [ "$fail_count" -gt 0 ]; then exit 1; fi
if [ "$fail_on_unavailable" -eq 1 ] && [ "$unavailable_count" -gt 0 ]; then exit 2; fi
exit 0
