---
name: build-audio-driven-share-course
description: Turn a long narration, recording, audio file, or narrated video into a synchronized, automatic, interactive web-based sharing course. Use when Codex must transcribe or analyze spoken content, split it into semantic scenes and timestamped cues, build or revise an HTML/React course driven by audio.currentTime, validate playback/seek/pause/responsive behavior, publish it, or iterate on feedback about pacing, motion, typography, density, and line wrapping.
---

# Build an audio-driven share course

Build a narrated sharing experience in which audio is the clock and the page is the stage. Preserve the speaker's meaning; do not add unsupported teaching points.

## Operating principles

- Treat the recording as the content authority and the only playback clock.
- Prefer semantic turns over fixed one- or two-minute cuts.
- Make every motion explain the current point: reveal, connect, expand, compare, focus, replace, archive, or conclude.
- Require only the initial play gesture. Keep later interaction optional and useful for review.
- Reconstruct state from `audio.currentTime`; never depend on accumulated timers.
- Preserve an existing site's stack, brand, URL, access level, and unrelated user changes.
- Fix systemic layout rules after feedback instead of patching only the reported screenshot.
- Treat every visible text block as video content. Validate it at short-video feed scale, especially right-side supporting copy.

## Phase 1: Audit inputs

1. Locate the source audio/video, current site or project, transcript artifacts, brand constraints, and publishing metadata.
2. Probe duration and audio availability. Use an existing transcript when it is trustworthy; otherwise transcribe in bounded chunks with available local or connected tooling.
3. If the source is long, first create rough two-minute analysis windows, then merge or split them at actual idea transitions.
4. Record uncertainties. Do not invent missing words, examples, or claims.
5. Keep the source media unchanged unless the user explicitly requests editing.

Pause only when the source cannot be accessed, transcription is impossible, or a missing choice would materially alter the course.

## Phase 2: Build the evidence map

For every rough segment, capture:

- start and end time;
- core claim;
- supporting example or contrast;
- important terms;
- natural visual metaphor;
- source excerpt or transcript range;
- uncertainty requiring review.

Convert the rough map into semantic scenes. Default to 30–75 seconds per scene, but let idea boundaries win. Aim for 3–6 cues per scene.

Read [scene-patterns.md](references/scene-patterns.md) when choosing visual structures.

## Phase 3: Freeze the timeline before animation

Create a canonical `timeline.json` that follows [timeline-schema.md](references/timeline-schema.md). Each scene must have contiguous start/end times and each cue must sit inside its scene.

Run:

```bash
node <skill-dir>/scripts/validate-timeline.mjs path/to/timeline.json
```

Do not begin detailed animation work while the validator reports errors. Use the emitted start/middle/end QA points for later browser checks.

## Phase 4: Design the experience

Use a full-stage layout with a compact header and bottom transport. Avoid a persistent presentation sidebar.

For each scene:

1. State one primary idea in the headline.
2. Show one dominant visual system.
3. Assign each cue one clear state change.
4. Delay supporting detail until the narration reaches it.
5. Let automatic panels, branches, or layers replace click-dependent accordions.

Typography rules:

- Read [short-video-readability.md](references/short-video-readability.md) whenever the output targets a mobile feed or the user reports unreadable text.
- Design for phone viewing after short-video downscaling, not only desktop proximity.
- Keep critical diagram text at least 18 CSS px on recording-size viewports when space permits; never rely on tiny labels for the main idea.
- Treat right-side labels, explanations, evidence, and annotations as readable content rather than decoration. Start from the same readable scale as the left content and reduce copy before reducing type.
- Use a short-video typography gate before animation polish: render representative frames for 390x844, 1086x1448 (3:4), and 1080x1920 (9:16) or the actual delivery sizes; inspect at 100% without zooming.
- If a viewer must pause, zoom, or move the phone close to read a right-side block, fail the gate. Fix the shared type scale, line height, container width, contrast, or copy length across all scenes.
- Use `text-wrap: pretty` for prose. Avoid balanced wrapping that turns a two-line Chinese headline into three cramped lines.
- At medium widths, let headlines use the full stage width. Keep short titles on one line when they fit.
- On wide layouts, insert optional semantic breaks after punctuation; remove those forced breaks at medium and mobile widths.
- Check for isolated characters, orphaned words, clipped labels, and detail panels covering core content.

Motion rules:

- Animate `transform` and `opacity` where practical.
- Use a single paused/running state for CSS motion.
- On manual seek, mark already-active cues as settled and render their final state immediately.
- Freeze in-progress motion when pausing; resume without restarting the scene.
- Cancel or replace stale scene motion after jumps.
- Honor `prefers-reduced-motion` with near-instant transitions.

## Phase 5: Implement from the clock

Keep the state function idempotent:

```text
rendered state = f(audio.currentTime, timeline)
```

Derive the current scene, active cues, automatic detail state, and progress from the current time. Support:

- play/pause;
- ±10 seconds;
- range seeking;
- scene navigation;
- keyboard play and seek when appropriate;
- audio loading, autoplay-blocked, and ended states.

Use the existing framework and dependencies. Add no heavy animation library unless the project already relies on it or the user explicitly requests it.

## Phase 6: Validate playback and visuals

Read and execute [qa-checklist.md](references/qa-checklist.md). At minimum:

1. Build the production output and run existing tests.
2. Check every scene at its start, midpoint, and end minus one second.
3. Verify pause freeze, resume, seek reconstruction, ±10 seconds, and scene jumps.
4. Inspect 1776×903 or the intended recording size, 1440×900, 1280×720, 933×766, and 390×844.
5. Check reduced motion, console errors, audio failure, and blocked autoplay.
6. Visually inspect representative definition, case, chain, architecture, resume, and final scenes.
7. Complete the short-video readability gate for Douyin, Kuaishou, and Xiaohongshu-style mobile viewing. Record failures by scene, region, and text role; do not sign off based on desktop preview alone.

When the user supplies a screenshot, reproduce that viewport before changing CSS. Compare the same scene and timestamp after the fix.

## Phase 7: Publish and hand off

If `.openai/hosting.json` exists, follow the installed Sites building and hosting skills. Reuse the existing project ID, URL, source branch, and access level. Build, commit, push, package, save one version, deploy privately when eligible, and poll to a terminal state.

Keep the local development server alive through deployment, then stop it. Return the live URL first and summarize only user-visible changes and validation results.

## Feedback loop

Classify feedback before editing:

- **Timing:** scene or cue is early, late, or too slow.
- **Meaning:** visual does not match the narration.
- **Density:** too much appears simultaneously.
- **Typography:** text is too small after downscaling.
- **Wrapping:** avoidable multi-line or non-semantic breaks.
- **Layout:** clipping, overlap, or missing content at a viewport.
- **Motion:** too weak, decorative, repetitive, or distracting.

Fix the shared cause, retest the reported viewport/time, then rerun the timeline matrix and production build before publishing.

For typography feedback, first identify the affected region (left content, right content, footer, diagram, or overlay) and role (headline, supporting copy, label, or evidence). When the right side is hard to read, enlarge the right-side system globally and simplify its copy; do not only enlarge the one screenshot that was reported.

## Deliverables

Produce the artifacts appropriate to the request:

- transcript or evidence map;
- validated semantic timeline;
- synchronized web course;
- reproducible QA evidence;
- short-video readability matrix covering phone scale, right-side text, wrapping, contrast, and platform-safe margins;
- deployed private URL when hosting is in scope.
