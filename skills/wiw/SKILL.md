---
name: wiw
description: Say in one sentence what the user actually wants, from the whole conversation and their wider situation, and keep that intent restorable in intent.md across long sessions, days, and loops.
disable-model-invocation: true
---

# WIW

WIW means "What I Want". Lead with the user's intent, then keep it.

## First, reread the user's own words

Before writing any sentence, run `python3 scripts/user_turns.py --max-chars 0` from this skill folder. It finds the current Codex or Claude Code transcript; pass the transcript path if it cannot. Read every user message, oldest first. A compaction summary, your memory of the conversation, or an earlier intent sentence is not a substitute; those are where the wrong sentence comes from.

While reading, mark the messages where the user explains why they want something, what they want for themselves, or how they want it done. Requests that only steer the work ("again", "start", "use this tool") matter less than the user's explanations.

## The intent sentence

State what the user wants to be true for them, then what is built or done to get there. A product, skill, or document is usually the means; do not make it the subject of the sentence when the user's goal is something it enables.

- Keep the user's own key words for what they want and how. Translate only metaphors, slang, and jokes into plain meaning. Do not replace the user's concrete words with a broader category that loses them.
- Durable: leave out people's names, dates, current bugs, and one-off examples, but keep a method or condition the user stated as part of what they want.
- Specific: a newcomer reading only this sentence should know what to build and what to leave out. A sentence that would fit any similar project is wrong.
- One sentence, two only if one cannot hold it.

## Answer first, with the evidence

Open with the intent sentence. Under it, quote the two to five user messages it rests on, short and verbatim, so the user can check the sentence against their own words in one glance. Add nothing else unless it helps that check.

## When the user says the sentence is wrong

Reread all user messages again and rebuild the sentence from them. Do not patch the previous sentence with the words of the latest correction; the previous sentence was built on a misreading, and the correction usually names only one symptom of it.

## Keep the intent

Write the sentence into the project's `intent.md` (shape in [assets/intent.md](assets/intent.md)), updating an existing file in place or creating one at the project root. Keep `Status: Draft` until the user explicitly confirms the sentence; only then set `Approved`. Record the date and the message numbers it rests on, and keep unconfirmed points under open questions. Do not ask whether to write the file; writing a draft is reversible.

Continue work toward an approved intent. With a draft that replaced a sentence the user rejected, wait for their check before changing other work to match it.

When work resumes after compaction, days, or a loop iteration, start from `intent.md` and reread the user's messages since its last update.

## With II

When II is also requested, II uses this sentence and `intent.md` to choose its expected answers. After the user confirms them, write the confirmed answers into the same `intent.md`. If a confirmed answer changes what is wanted, rewrite the sentence here.
