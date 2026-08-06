# Timeline schema

Use JSON as the canonical editorial contract even when the application later converts it to TypeScript.

## Shape

```json
{
  "duration": 709,
  "source": "public/share.mp3",
  "scenes": [
    {
      "id": "01",
      "start": 0,
      "end": 31,
      "eyebrow": "岗位正在改变",
      "title": "FDE，不只是开发",
      "summary": "把模糊业务问题做成可上线、可使用的系统。",
      "detailAt": 24,
      "detail": "来自当前语音段落的补充。",
      "layout": "definition-build",
      "sourceRange": "00:00-00:31",
      "cues": [
        { "at": 2, "action": "reveal", "target": "old-role", "label": "传统开发" },
        { "at": 8, "action": "replace", "target": "role", "label": "FDE 组合" },
        { "at": 18, "action": "connect", "target": "delivery-path", "label": "问题到系统" }
      ]
    }
  ]
}
```

## Invariants

- `duration` is finite and positive.
- Scene IDs are unique and ordered.
- The first scene starts at zero.
- Scenes are contiguous and non-overlapping.
- The final scene ends at `duration` within 0.5 seconds.
- Every scene has a non-empty title and 3–6 ordered cues.
- Every cue time is absolute and satisfies `scene.start <= cue.at < scene.end`.
- `detailAt`, when present, sits inside the scene.
- Cue labels and scene copy are supported by `sourceRange` or the evidence map.

## Recommended cue actions

- `reveal`: introduce a term, person, object, or fact.
- `replace`: retire a weaker concept and emphasize a stronger one.
- `connect`: grow a process, dependency, or system path.
- `expand`: expose hidden complexity or a detail layer.
- `compare`: present a before/after or left/right distinction.
- `focus`: dim context and foreground the current conclusion.
- `archive`: move evidence into a persistent record.
- `finalize`: settle the scene into its concluding state.

Action names guide design; they do not prescribe a component API.

## State reconstruction

At any time `t`:

1. Select the scene where `start <= t < end`; select the last scene at the exact duration.
2. Activate cues where `cue.at <= t`.
3. Open automatic detail when `t >= detailAt`, unless a deliberate review override exists.
4. Render active cues from state, not from previous events.
5. After manual seek, render active cues in their settled end state; future cues may animate normally.

