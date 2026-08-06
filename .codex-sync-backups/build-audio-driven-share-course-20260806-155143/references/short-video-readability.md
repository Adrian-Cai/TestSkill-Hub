# Short-video readability workflow

Use this reference whenever the course will be watched in a Douyin-, Kuaishou-, or Xiaohongshu-style mobile feed, or whenever the user reports that text is too small.

## 1. Inventory text by role and region

Before polishing motion, list every visible text block in representative scenes:

- **Primary:** scene headline or one-sentence takeaway.
- **Supporting:** explanation, example, contrast, or evidence.
- **Structural:** diagram labels, badges, node names, checks, and status text.
- **Controls:** transport, buttons, progress, and navigation.

Mark each block as left, right, full-width, diagram, or overlay. Do not assume that right-side text is secondary just because it is positioned on the right; if it carries meaning from the narration, it must pass the same readability gate.

## 2. Compose for the feed, not the editor

Use a mobile-first hierarchy:

1. Keep one clear takeaway per frame.
2. Give the right-side content enough width and type size to be read without zooming.
3. Remove repeated or decorative microcopy before shrinking text.
4. Prefer two comfortable lines over three cramped lines.
5. Break Chinese copy at punctuation or meaning boundaries; never leave isolated characters or orphaned short phrases.
6. Reserve breathing room near edges and likely platform UI overlays.

For text-heavy content, render exact text with HTML/CSS or another deterministic text layer. Use generated artwork for background or visual structure, then overlay final copy so spelling, size, and wrapping remain controllable.

## 3. Use practical starting values

Treat these as starting points, not universal absolutes. Tune against the actual composition and delivery size:

| Text role | Starting scale on a 1080–1440 design canvas | Guidance |
| --- | ---: | --- |
| Primary headline | 48–72 px | Keep to one or two semantic lines. |
| Supporting copy | 28–40 px | Limit the number of lines and avoid dense paragraphs. |
| Right-side explanatory text | 26–36 px | Never let this become a tiny annotation column. |
| Diagram labels / evidence | 22–30 px | Merge, remove, or reveal progressively if crowded. |
| Controls | 22 px or larger where visible in the video | Keep labels short and high contrast. |

At recording-size viewports, critical text should generally remain at least 18 CSS px. If the frame is still difficult to read at phone scale, increase the size or shorten the copy even when the CSS value technically passes.

## 4. Run the platform readability gate

For each representative scene, render at:

- the actual recording viewport;
- 1086x1448 for a 3:4 vertical asset when applicable;
- 1080x1920 for a 9:16 vertical asset when applicable;
- 390x844 as a phone-scale inspection viewport.

Inspect at 100% with no browser zoom. For each size, check:

- the left and right text blocks can be read immediately;
- right-side supporting copy is not visibly smaller than the surrounding visual hierarchy;
- contrast survives downscaling and compression;
- no text is hidden under edge margins or platform controls;
- no line is clipped, overcrowded, or broken at an unnatural point;
- the frame remains understandable when viewed briefly in a scrolling feed.

Classify the result as **pass**, **conditional** (readable but crowded), or **fail** (requires pause/zoom or cannot be read). Any fail blocks delivery.

## 5. Fix feedback systemically

When a user says “the right-side text is too small”:

1. Reproduce the same scene at phone scale.
2. Confirm whether the issue is type size, line height, width, contrast, copy length, or platform cropping.
3. Update the shared component or design token used by the affected region.
4. Recheck at least one short, one medium, and one dense scene.
5. Rerun the full scene matrix before publishing.

Do not solve the issue by enlarging only one screenshot or by adding more words to compensate for a visual gap.
