# QA checklist

## Content fidelity

- Every headline, example, and conclusion is traceable to the recording.
- No cue reveals information before the narration introduces it.
- Scene boundaries follow idea changes rather than equal durations.
- The final scene ends with the recording rather than an arbitrary timer.

## Timeline reconstruction

- Validate the canonical timeline with `validate-timeline.mjs`.
- Visit every scene at start, midpoint, and end minus one second.
- Seek forward and backward while paused; the destination must not be blank.
- Seek into a scene after several cues; prior cues must appear settled immediately.
- Resume after a seek; future cues animate once and stale motion does not return.

## Playback

- Initial play works after one user gesture.
- Pause freezes audio and in-progress motion.
- Resume continues from the same state.
- ±10 seconds and range seeking update scene, cue, details, and progress.
- Scene navigation lands at the intended start time.
- Audio loading failure and blocked autoplay show recoverable guidance.
- Ending leaves a deliberate final state.

## Visual matrix

Inspect at least:

- intended recording viewport, commonly 1776×903 or 1920×1080;
- 1440×900;
- 1280×720;
- 933×766 for narrow desktop or in-app side panels;
- 390×844 for mobile.

At each size check:

- critical text remains readable after short-video downscaling;
- right-side explanatory text is readable without pausing or zooming;
- the text hierarchy remains valid on Douyin-, Kuaishou-, and Xiaohongshu-style mobile feeds;
- platform-safe margins keep text away from likely UI overlays and edge crops;
- short headings remain on one line when space permits;
- long Chinese headings break at punctuation or semantic boundaries;
- no isolated character sits on its own line;
- detail panels do not cover the primary visual;
- flow labels, checks, and evidence lists are not clipped;
- the transport remains reachable without hiding core content.

## Short-video typography gate

For every representative scene, classify visible text by role and region, then record:

- target delivery ratio (3:4, 9:16, or the actual requested ratio);
- rendered size and phone-scale viewport used for inspection;
- right-side text result: pass, conditional, or fail;
- any issue with size, line height, contrast, wrapping, clipping, or platform-safe margin;
- the shared rule or component changed to fix it.

Fail the gate when any meaningful text requires zooming, pausing, or close inspection to read. Reduce copy or enlarge the shared type scale before finalizing motion and publishing.

Check representative scenes for definition, obstacle stack, case expansion, lifecycle chain, human review, evidence archive, resume, transformation, and final action.

## Motion and accessibility

- Scene transitions have no cross-scene residue.
- Motion explains the narration and is not decorative repetition.
- `prefers-reduced-motion` shortens transitions and avoids large movement.
- Keyboard controls do not hijack focused form fields.
- Buttons and range controls have accessible names and visible focus states.

## Technical and publishing

- Production build succeeds.
- Existing automated tests pass.
- Browser console has no errors or warnings caused by the course.
- Source state, build archive, saved version, and deployed version match.
- Existing private/public access level and URL are preserved unless the user asks to change them.
