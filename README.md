# WIW + II

Two small agent skills for Codex, Claude Code and other agents that read `SKILL.md`.

- **WIW (What I Want)**: rereads your own messages in the current session, states in one sentence what you actually want, and keeps it in `intent.md` so the goal survives long sessions, days and context compaction.
- **II (Inverted Interview)**: instead of waiting for you to explain everything, the agent finds what the two of you have not discussed yet (unstated premises, undecided points, gaps), asks each one with its expected answer, and repeats until nothing is left open.

They work well together: WIW sets the intent, II closes every gap against it before the agent builds.

## Install

```bash
npx skills add sergiobuilds/wiw-ii
```

Or copy `skills/wiw` and `skills/ii` into your agent's skills folder (for Codex: `~/.codex/skills/`, for Claude Code: `~/.claude/skills/`).

## Use

```
$wiw   what am I actually trying to do here?
$ii    ask me everything we have not decided yet
```

Both skills are invoked explicitly; they do not trigger on their own.

---

## 한국어

- **WIW (What I Want)**: 지금 대화에서 사용자가 쓴 말을 처음부터 다시 읽고, 정말 원하는 것을 한 문장으로 세워 `intent.md`에 남깁니다. 긴 세션, 며칠 뒤, 맥락 압축 뒤에도 목표가 흐려지지 않습니다.
- **II (Inverted Interview, 인버티드 인터뷰)**: 사용자가 다 설명하기를 기다리지 않고, 에이전트가 아직 논의하지 않은 전제·정해지지 않은 점·부족한 점을 먼저 찾아 예상 답과 함께 묻습니다. 빈틈이 하나도 남지 않을 때까지 반복합니다.

설치: `npx skills add sergiobuilds/wiw-ii`

Made by the [Ouroboros](https://github.com/Q00/ouroboros) team. MIT License.

