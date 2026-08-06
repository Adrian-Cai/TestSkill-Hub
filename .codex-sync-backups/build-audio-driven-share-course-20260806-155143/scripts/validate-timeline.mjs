#!/usr/bin/env node

import { readFile } from "node:fs/promises";
import process from "node:process";

const file = process.argv[2];
if (!file) {
  console.error("Usage: node validate-timeline.mjs <timeline.json>");
  process.exit(2);
}

let timeline;
try {
  timeline = JSON.parse(await readFile(file, "utf8"));
} catch (error) {
  console.error(`Cannot read timeline: ${error.message}`);
  process.exit(2);
}

const errors = [];
const warnings = [];
const duration = Number(timeline.duration);
const scenes = timeline.scenes;
const tolerance = 0.1;

if (!Number.isFinite(duration) || duration <= 0) errors.push("duration must be a positive number");
if (!Array.isArray(scenes) || scenes.length === 0) errors.push("scenes must be a non-empty array");

const ids = new Set();
const qaPoints = [];

if (Array.isArray(scenes)) {
  scenes.forEach((scene, index) => {
    const path = `scenes[${index}]`;
    const start = Number(scene.start);
    const end = Number(scene.end);

    if (typeof scene.id !== "string" || !scene.id) errors.push(`${path}.id must be a non-empty string`);
    else if (ids.has(scene.id)) errors.push(`${path}.id must be unique`);
    else ids.add(scene.id);

    if (typeof scene.title !== "string" || !scene.title.trim()) errors.push(`${path}.title must be non-empty`);
    if (!Number.isFinite(start) || !Number.isFinite(end) || start < 0 || end <= start) {
      errors.push(`${path} must have finite times with 0 <= start < end`);
      return;
    }

    if (index === 0 && Math.abs(start) > tolerance) errors.push("the first scene must start at 0");
    if (index > 0) {
      const previousEnd = Number(scenes[index - 1].end);
      if (Number.isFinite(previousEnd) && Math.abs(previousEnd - start) > tolerance) {
        errors.push(`${path}.start must equal the previous scene end`);
      }
    }

    if (scene.detailAt !== undefined) {
      const detailAt = Number(scene.detailAt);
      if (!Number.isFinite(detailAt) || detailAt < start || detailAt >= end) {
        errors.push(`${path}.detailAt must be inside the scene`);
      }
    }

    if (!Array.isArray(scene.cues)) {
      errors.push(`${path}.cues must be an array`);
    } else {
      if (scene.cues.length < 3 || scene.cues.length > 6) {
        warnings.push(`${path} should normally contain 3-6 cues; found ${scene.cues.length}`);
      }
      let previousCue = -Infinity;
      scene.cues.forEach((cue, cueIndex) => {
        const cueAt = Number(cue.at);
        const cuePath = `${path}.cues[${cueIndex}]`;
        if (!Number.isFinite(cueAt) || cueAt < start || cueAt >= end) {
          errors.push(`${cuePath}.at must be inside the scene`);
        }
        if (cueAt < previousCue) errors.push(`${path}.cues must be ordered by time`);
        previousCue = cueAt;
        if (typeof cue.action !== "string" || !cue.action) errors.push(`${cuePath}.action must be non-empty`);
        if (typeof cue.target !== "string" || !cue.target) errors.push(`${cuePath}.target must be non-empty`);
      });
    }

    qaPoints.push({
      id: scene.id,
      start,
      middle: Number(((start + end) / 2).toFixed(2)),
      end_minus_one: Number(Math.max(start, end - 1).toFixed(2)),
    });
  });
}

if (Array.isArray(scenes) && scenes.length && Number.isFinite(duration)) {
  const finalEnd = Number(scenes.at(-1).end);
  if (!Number.isFinite(finalEnd) || Math.abs(finalEnd - duration) > 0.5) {
    errors.push("the final scene end must match duration within 0.5 seconds");
  }
}

const result = {
  valid: errors.length === 0,
  duration,
  scene_count: Array.isArray(scenes) ? scenes.length : 0,
  qa_point_count: qaPoints.length * 3,
  qa_points: qaPoints,
  warnings,
  errors,
};

console.log(JSON.stringify(result, null, 2));
process.exit(errors.length ? 1 : 0);

