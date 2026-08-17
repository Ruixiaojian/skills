#!/usr/bin/env python3
"""Content-driven timing for Vox Video Director.

Estimate a narration segment from text before TTS, then replace the estimate with
the measured narration audio duration. New projects use one 5-10 second video clip
per beat; text that needs more than 10 seconds must be split into another beat.
"""
import argparse
import json
import math
import os
import re


def _cfg(doc):
    cfg = doc.get("timing", {})
    return {
        "mode": doc.get("timing_mode", cfg.get("mode", "content")),
        "min": float(cfg.get("min_segment", 5)),
        "max": float(cfg.get("max_segment", 10)),
        "tail": float(cfg.get("tail", 0.45)),
        "cjk_cps": float(cfg.get("cjk_chars_per_second", 4.2)),
        "word_wps": float(cfg.get("latin_words_per_second", 2.5)),
    }


def spoken_seconds(text, language=None, cjk_cps=4.2, word_wps=2.5):
    """Estimate speech only; pauses are counted, but no edit tail is added."""
    text = text or ""
    cjk = len(re.findall(r"[\u3400-\u9fff]", text))
    latin_words = len(re.findall(r"[A-Za-z0-9]+(?:[-_.][A-Za-z0-9]+)*", text))
    seconds = cjk / cjk_cps + latin_words / word_wps
    seconds += len(re.findall(r"[,，、;；:]", text)) * 0.10
    seconds += len(re.findall(r"[.!?。！？]", text)) * 0.22
    return round(seconds, 3)


def _ceil_half(value):
    return math.ceil(value * 2.0) / 2.0


def resolve_beat_duration(beat, doc, prefer_audio=True):
    cfg = _cfg(doc)
    if cfg["mode"] != "content":
        return None, None
    measured = beat.get("narration_dur") if prefer_audio else None
    speech = float(measured) if measured is not None else spoken_seconds(
        beat.get("narration", ""), doc.get("language"), cfg["cjk_cps"], cfg["word_wps"]
    )
    raw = speech + cfg["tail"]
    if raw > cfg["max"]:
        return None, (
            f"beat {beat.get('id')} needs about {raw:.2f}s, above the {cfg['max']:.0f}s "
            "segment limit; split its narration into two beats"
        )
    return round(max(cfg["min"], min(cfg["max"], _ceil_half(raw))), 2), None


def apply_content_timing(doc, prefer_audio=True):
    """Write dynamic durations. Preserve explicit legacy multi-shot timing."""
    if _cfg(doc)["mode"] != "content":
        return []
    issues = []
    for beat in doc.get("beats", []):
        dur, issue = resolve_beat_duration(beat, doc, prefer_audio=prefer_audio)
        if issue:
            issues.append(issue)
            continue
        beat["dur"] = dur
        shots = beat.get("shots") or []
        if len(shots) == 1 and not shots[0].get("dur_locked"):
            shots[0]["dur"] = dur
        elif len(shots) > 1 and not all("dur" in shot for shot in shots):
            # Compatibility only: new content-driven projects should use one shot
            # per beat. Older multi-shot projects may still use 3s+ model clips.
            each = round(dur / len(shots), 2)
            if each < 3:
                issues.append(
                    f"beat {beat.get('id')} has {len(shots)} shots but only {dur:.1f}s; "
                    "use one shot or provide explicit durations of at least 3s"
                )
            else:
                for shot in shots:
                    shot.setdefault("dur", each)
    doc["timing_issues"] = issues
    return issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project_dir")
    ap.add_argument("--estimated", action="store_true", help="ignore measured narration_dur")
    args = ap.parse_args()
    path = os.path.join(args.project_dir, "beats.json")
    with open(path, encoding="utf-8") as f:
        doc = json.load(f)
    issues = apply_content_timing(doc, prefer_audio=not args.estimated)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    for beat in doc.get("beats", []):
        print(f"beat {beat.get('id')}: {beat.get('dur', 'SPLIT')}s")
    if issues:
        print("TIMING ISSUES:")
        for issue in issues:
            print("-", issue)
        raise SystemExit(2)


if __name__ == "__main__":
    main()
