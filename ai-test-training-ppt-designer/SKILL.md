---
name: ai-test-training-ppt-designer
description: Design enterprise internal training chapters, PPT structures, detailed slide plans, instructor scripts, classroom controls, and final PPT decks for AI-enabled software testing courses. Use when the user provides a chapter input card, course topic, training module brief, or asks to generate AI software testing training materials such as "课程章节设计", "PPT结构蓝图", "逐页PPT详细设计", "讲师授课稿", "课堂互动", or a 4:3 PPT课件文件.
---

# AI测试内训课件设计

## Overview

Use this skill to turn an AI-enabled software testing training brief into a professional enterprise training chapter and, when requested, a finished PPT deck.

The core workflow is:

```text
chapter input card -> chapter design -> PPT blueprint -> slide detail design -> instructor script -> PPT file
```

Always keep the course grounded in software testing work. Explain how AI embeds into testing activities; do not turn the material into a generic AI course.

## Core Principles

- Use real testing workflow language: requirements review, rules extraction, test point matrix, risk sorting, test case optimization, defect analysis, regression scope.
- Every method must show the loop: input -> AI processing -> human review -> testing output.
- Treat AI as an assistant, not a replacement. AI drafts, organizes, expands, checks, and summarizes. Testers own business judgment, risk judgment, quality responsibility, and final confirmation.
- Keep the tone professional, restrained, and practical for enterprise internal training.
- If the input card and chapter name conflict, explicitly point it out first and recommend a correction before generating content.
- Do not generate PPT page content, instructor scripts, or a PPT file unless the user asks for that stage.

## Workflow

### Step 1: Validate the chapter input

Check whether the user supplied enough information:

- course topic
- chapter name
- chapter positioning
- core problem
- core methods
- training actions
- case scenario
- deliverables
- target learners and duration, if available

If information is missing but the task can proceed, make conservative assumptions and mark them. Ask only when the missing information would materially change the design.

### Step 2: Produce chapter design

When asked for "课程章节设计", output only:

- chapter positioning, including role in the whole course, what it inherits from the prior chapter, and what it leads to next
- core problem in testing practitioners' language
- 3-6 core methods, each written as input -> AI processing -> human review -> final output
- recommended classroom case and why it fits the duration
- 3-5 training actions
- chapter deliverables tightly related to the module

Do not write PPT pages or a full instructor script at this stage.

### Step 3: Produce PPT structure blueprint

When asked for "PPT结构蓝图", create a 6-7 page structure unless the user specifies otherwise.

Each page must have one clear consulting-style claim. Use the testing workflow as the page order, for example:

1. why this testing activity is a high-value AI entry point
2. the real tester pain point
3. the controlled AI collaboration loop
4. requirement summary and rule extraction
5. test point matrix construction
6. risk and requirement-question exposure
7. classroom practice and deliverables

Use the table fields requested by the user. Keep visible slide copy short and audience-facing.

### Step 4: Produce detailed slide design

When asked for "逐页PPT详细设计", provide for each slide:

- page title
- core point
- 3-5 short PPT copy points
- recommended layout
- visual style
- instructor oral focus
- suggested time
- transition to the next slide

Use a premium enterprise training and consulting presentation style:

- 4:3 ratio when the user asks for a file
- clean white space
- low-saturation palette
- soft gradient backgrounds
- light cards
- thin lines
- process arrows
- matrix tables
- risk grids

Avoid robot, brain, circuit board, neon, and 3D cartoon AI visuals.

### Step 5: Produce instructor script and classroom controls

When asked for "讲师授课稿" or "课堂控制", write a 12-15 minute script for a 15-minute module unless the user specifies another duration.

Include:

- page-by-page oral script
- one classroom interaction only, unless the user requests more
- where to ask it, expected learner responses, how to receive responses, recovery wording, and transition
- time control advice
- what not to over-expand
- what must be emphasized
- what belongs in later chapters
- the chapter deliverable list

Keep the script practical and tied to testing examples. Do not over-explain AI theory.

### Step 6: Generate a PPT file

When the user asks for an actual PPT file:

- Use the `presentations` skill/tooling if available.
- Create an editable `.pptx`, not a deck made of flattened screenshots.
- Follow the confirmed slide titles and content exactly; do not redesign the course structure unless the user asks.
- Use 4:3 ratio when specified.
- Render and inspect the final slides before delivery.
- Fix overflow, clipping, awkward wrapping, and unintended overlap before returning the file path.
- Save final user-facing deliverables to the user-requested location, or to the workspace `outputs/` directory when no location is specified.

## Required Reference

For exact output schemas, page archetypes, wording constraints, and PPT quality gates, read `references/workflow-templates.md` when producing any structured chapter, PPT blueprint, detailed slide plan, instructor script, or PPT file.

When the user asks what learners should take away after a chapter, or when generating learner-facing materials after a training module, read `references/deliverables-checklist.md` and include a focused deliverables list.

## Quality Gate

Before finalizing any output, check:

- The content follows the testing workflow rather than a generic AI lecture flow.
- Each method keeps input -> AI processing -> human review -> output visible.
- Slide titles are judgmental and specific, not generic labels.
- AI responsibility and tester responsibility are clearly separated.
- Classroom cases are feasible within the target duration.
- Deliverables are directly related to the chapter.
- Learner-facing deliverables are explicit enough to use after class, not only mentioned in the instructor script.
- PPT file outputs have passed visual/render validation when generated.
