#!/usr/bin/env python3
"""HMTL - Pre-flight Token Gatekeeper.

Reports remaining context budget for the current agent session.

Backends
  claude       exact, parsed from ~/.claude/projects/**/*.jsonl `usage` records
  antigravity  ESTIMATE, derived from transcript size (no usage telemetry exists)

Usage
  hmtl.py [--json] [--source auto|claude|antigravity] [--limit N]
"""
import json
import os
import sys
from pathlib import Path

CLAUDE_LIMIT = 200_000
ANTIGRAVITY_LIMIT = 1_000_000
BYTES_PER_TOKEN = 3.5  # mixed Korean/English/code UTF-8 heuristic


# --------------------------------------------------------------------------
# Claude Code backend (exact)
# --------------------------------------------------------------------------
def claude_session_file():
    d = Path.home() / ".claude" / "projects"
    if not d.exists():
        return None
    files = list(d.glob("**/*.jsonl"))
    return max(files, key=os.path.getmtime) if files else None


def claude_usage(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except OSError:
        return None, None
    for line in reversed(lines[-200:]):
        try:
            data = json.loads(line)
        except ValueError:
            continue
        msg = data.get("message")
        if isinstance(msg, dict) and msg.get("usage"):
            return msg.get("model"), msg["usage"]
        if data.get("usage"):
            return data.get("model"), data["usage"]
    return None, None


def read_claude(limit):
    path = claude_session_file()
    if not path:
        return {"error": "No Claude session log found under ~/.claude/projects"}
    model, usage = claude_usage(path)
    if not usage:
        return {"error": "No usage record found in Claude session log"}

    cache_read = usage.get("cache_read_input_tokens", 0)
    cache_create = usage.get("cache_creation_input_tokens", 0)
    direct_input = usage.get("input_tokens", 0)
    output_tokens = usage.get("output_tokens", 0)
    total = cache_read + cache_create + direct_input

    return {
        "source": "claude",
        "accuracy": "exact",
        "model": model or "unknown",
        "session_file": str(path),
        "context_limit": limit or CLAUDE_LIMIT,
        "total_context": total,
        "breakdown": {
            "cache_read": cache_read,
            "cache_create": cache_create,
            "direct_input": direct_input,
            "output_tokens": output_tokens,
        },
    }


# --------------------------------------------------------------------------
# Antigravity backend (estimate)
# --------------------------------------------------------------------------
def antigravity_transcript():
    root = Path.home() / ".gemini" / "antigravity-cli" / "brain"
    if not root.exists():
        return None
    files = list(root.glob("*/.system_generated/logs/transcript.jsonl"))
    return max(files, key=os.path.getmtime) if files else None


def antigravity_model():
    cfg = Path.home() / ".gemini" / "antigravity-cli" / "settings.json"
    try:
        return json.loads(cfg.read_text(encoding="utf-8")).get("model")
    except Exception:
        return None


def read_antigravity(limit):
    path = antigravity_transcript()
    if not path:
        return {"error": "No Antigravity transcript found under ~/.gemini/antigravity-cli/brain"}

    raw = path.read_bytes()
    steps = sum(1 for line in raw.splitlines() if line.strip())
    est = int(len(raw) / BYTES_PER_TOKEN)

    return {
        "source": "antigravity",
        "accuracy": "estimate",
        "accuracy_note": (
            "Antigravity stores no token usage telemetry. This is derived from "
            "transcript byte size at ~%.1f bytes/token; assume +/-30%% error."
            % BYTES_PER_TOKEN
        ),
        "model": antigravity_model() or "unknown",
        "session_file": str(path),
        "context_limit": limit or ANTIGRAVITY_LIMIT,
        "total_context": est,
        "breakdown": {
            "transcript_bytes": len(raw),
            "transcript_steps": steps,
            "bytes_per_token": BYTES_PER_TOKEN,
        },
    }


# --------------------------------------------------------------------------
def detect_source():
    c = claude_session_file()
    a = antigravity_transcript()
    if c and a:
        return "claude" if os.path.getmtime(c) >= os.path.getmtime(a) else "antigravity"
    if c:
        return "claude"
    if a:
        return "antigravity"
    return None


def arg_value(flag, default=None):
    if flag in sys.argv:
        i = sys.argv.index(flag)
        if i + 1 < len(sys.argv):
            return sys.argv[i + 1]
    return default


def main():
    as_json = "--json" in sys.argv
    source = arg_value("--source", "auto")
    limit = arg_value("--limit")
    limit = int(limit) if limit else None

    if source == "auto":
        source = detect_source()
        if source is None:
            fail({"error": "No Claude or Antigravity session found"}, as_json)

    if source == "claude":
        result = read_claude(limit)
    elif source == "antigravity":
        result = read_antigravity(limit)
    else:
        fail({"error": "Unknown --source %r (use auto|claude|antigravity)" % source}, as_json)

    if "error" in result:
        fail(result, as_json)

    total = result["total_context"]
    ctx_limit = result["context_limit"]
    result["tokens_left"] = max(0, ctx_limit - total)
    result["percent_used"] = round(total / ctx_limit * 100, 2)

    if as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    render(result)


def fail(result, as_json):
    if as_json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print("[X] " + result["error"])
    sys.exit(1)


def render(r):
    bar_len = 20
    ratio = r["total_context"] / r["context_limit"]
    filled = min(bar_len, max(0, int(round(bar_len * ratio))))
    gauge = "#" * filled + "-" * (bar_len - filled)
    tag = "EXACT" if r["accuracy"] == "exact" else "ESTIMATE"

    print("=" * 62)
    print("[HMTL] Context Token Monitor  --  %s (%s)" % (r["source"], tag))
    print("=" * 62)
    print("Model       : %s" % r["model"])
    print("Window Limit: {:,} tokens".format(r["context_limit"]))
    print("Usage Gauge : [{}] {:.1f}%  ({:,} / {:,})".format(
        gauge, r["percent_used"], r["total_context"], r["context_limit"]))
    print("Tokens Left : {:,} tokens ({:.1f}% left)".format(
        r["tokens_left"], 100 - r["percent_used"]))
    print("-" * 62)
    for k, v in r["breakdown"].items():
        print("  {:<16}: {:,}".format(k, v) if isinstance(v, int)
              else "  {:<16}: {}".format(k, v))
    if r.get("accuracy_note"):
        print("-" * 62)
        print("  NOTE: " + r["accuracy_note"])
    print("=" * 62)


if __name__ == "__main__":
    main()
