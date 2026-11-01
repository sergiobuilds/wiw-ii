#!/usr/bin/env python3
"""Print the user's own messages from the current Codex or Claude Code session, oldest first.

WIW rereads these instead of trusting memory or a compaction summary.
"""
import argparse
import glob
import json
import os
import sys

INJECTED = (
    "<environment_context", "<permissions", "<collaboration_mode", "<skills_instructions",
    "<user_instructions", "<turn_aborted", "<model_switch", "<model_instructions",
    "<codex_apps", "<external_codex", "<app-context", "<system-reminder", "<command-",
    "<local-command", "<skill>", "# AGENTS.md", "<INSTRUCTIONS>",
    "Caveat: The messages below", "<send_user_message_question_reply",
)
INJECTED_PREFIXES = ("Warning: truncated output", "## Project Instructions")


def own_text(text):
    """Strip harness blocks the client appends after the user's words."""
    cut = len(text)
    for marker in INJECTED + INJECTED_PREFIXES:
        i = text.find(marker)
        if i > 0:
            cut = min(cut, i)
    text = text[:cut].strip()
    if not text or text.startswith(INJECTED + INJECTED_PREFIXES):
        return ""
    return text


def codex_turns(path):
    for line in open(path, encoding="utf-8"):
        d = json.loads(line)
        p = d.get("payload") or {}
        if d.get("type") == "response_item" and p.get("type") == "message" and p.get("role") == "user":
            text = "\n".join(c.get("text", "") for c in p.get("content", []) if c.get("type") == "input_text")
            yield d.get("timestamp", ""), text


def claude_turns(path):
    for line in open(path, encoding="utf-8"):
        d = json.loads(line)
        if d.get("type") != "user" or d.get("isMeta") or d.get("isSidechain") or d.get("isCompactSummary"):
            continue
        m = d.get("message", {}).get("content")
        text = m if isinstance(m, str) else "\n".join(c.get("text", "") for c in m or [] if c.get("type") == "text")
        yield d.get("timestamp", ""), text


def find_session(arg, session_id):
    if arg:
        if not os.path.isfile(arg):
            sys.exit(f"Transcript not found: {arg}")
        return arg, ("claude" if "/.claude/" in arg else "codex")
    codex_home = os.environ.get("CODEX_HOME") or os.path.expanduser("~/.codex")
    thread = os.environ.get("CODEX_THREAD_ID")
    if thread:
        hits = glob.glob(os.path.join(codex_home, "sessions", "**", f"*{thread}.jsonl"), recursive=True)
        if hits:
            return hits[0], "codex"
    # Claude Code exposes the live session to subprocesses; a skill can also pass ${CLAUDE_SESSION_ID}.
    claude_id = session_id if session_id and not session_id.startswith("$") else os.environ.get("CLAUDE_CODE_SESSION_ID")
    if claude_id:
        hits = glob.glob(os.path.expanduser(f"~/.claude/projects/*/{claude_id}.jsonl"))
        if hits:
            return hits[0], "claude"
        sys.exit(f"Claude session {claude_id} has no transcript yet. Pass the transcript path explicitly.")
    slug = os.getcwd().replace("/", "-").replace(".", "-")
    hits = sorted(glob.glob(os.path.expanduser(f"~/.claude/projects/{slug}/*.jsonl")), key=os.path.getmtime)
    if hits:
        print("# warning: no session id; using the most recently modified Claude transcript for this folder", file=sys.stderr)
        return hits[-1], "claude"
    sys.exit("No session found. Pass the transcript path explicitly.")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("session", nargs="?", help="transcript .jsonl path; default: current session")
    ap.add_argument("--session-id", help="Claude Code session id; defaults to CLAUDE_CODE_SESSION_ID")
    ap.add_argument("--max-chars", type=int, default=1500, help="truncate each message (0 = no limit)")
    args = ap.parse_args()
    path, kind = find_session(args.session, args.session_id)
    turns = codex_turns(path) if kind == "codex" else claude_turns(path)
    print(f"# {kind} session: {path}")
    n = 0
    for ts, raw in turns:
        text = own_text(raw)
        if not text:
            continue
        n += 1
        if args.max_chars and len(text) > args.max_chars:
            text = text[: args.max_chars] + " …[truncated]"
        print(f"\n[{n}] {ts[:19].replace('T', ' ')}\n{text}")
    if n == 0:
        print("(no user messages found)")


if __name__ == "__main__":
    main()
