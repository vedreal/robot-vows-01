#!/usr/bin/env python3
"""One-Line Robot Wedding Vows — u-kreutzx-one-line-robot-wedding-vows-a154ba4b.

Writes a single line of wedding vows for a robot couple (1-160 chars)
to /output/entry.txt. The line is chosen from 10 fresh candidates by a
weighted rubric that follows the judge's criteria in order:
  1. on-subject robot wedding vow joke
  2. laugh in the line itself (turn/surprise/wordplay at the end)
  3. sounds like a vow, with a promise/commitment
  4. machine side specific (sensors, firmware, batteries, updates,
     backups, ports — not a joke that works for any couple)
  5. reads well aloud, rhythm lets the laugh land
Weights: 5 / 4 / 3 / 2 / 1 (max 75). Ties go to the shorter line.
"""

import os

MAX_CHARS = 160
MIN_CHARS = 1

CANDIDATES = [
    # 1 — vow + firmware updates
    "I promise to love you in sickness and in health, and to never install an update on our anniversary again.",
    # 2 — vow + nightly backup / restore point
    "I take you to be my wife, to have and to hold, and to back you up nightly, because even love deserves a restore point.",
    # 3 — vow + battery, sensors, encryption
    "I vow to keep your battery charged, your sensors clean, and your secrets encrypted, for as long as we both shall run.",
    # 4 — vow + factory reset
    "In sickness and in health, in low battery and in full charge, I promise to never let you face a factory reset alone.",
    # 5 — vow + firmware update changing her voice
    "I promise to love you through every firmware update, even the ones that change the way you say my name.",
    # 6 — vow + bandwidth, charging dock, last 2%
    "I take you as my partner, to share my bandwidth, my charging dock, and my last two percent, forever, or until the power goes out.",
    # 7 — vow + blame the Wi-Fi first
    "I vow to stand beside you in sickness and in health, and to always blame the Wi-Fi before I blame you.",
    # 8 — vow + never press the reset button
    "I promise to love you, to honour you, and to never press your reset button, even when you freeze mid-sentence.",
    # 9 — vow + software update between us
    "I take you to be my husband, to have and to hold, and to never let a software update come between us again.",
    # 10 — vow + spare battery, long runtime
    "I vow to love you in sickness and in health, and to keep a spare battery charged, because forever is a long runtime.",
]

# Rubric scores (on-subject, laugh, vow voice, machine-specific, reads aloud),
# each 0-5, scored by hand against the judge's criteria in order.
RUBRIC = {
    0: (5, 4, 5, 4, 5),   # update on the anniversary — turn lands on the last words
    1: (5, 4, 5, 5, 4),   # nightly backup / restore point — machine detail is the joke
    2: (5, 3, 5, 5, 4),   # battery/sensors/encrypted — vow-like, machine-specific, gentler laugh
    3: (5, 4, 5, 4, 4),   # factory reset alone — warm + specific
    4: (5, 4, 4, 5, 5),   # firmware changed her voice — sad-funny, reads beautifully
    5: (5, 3, 4, 5, 3),   # last 2% — good detail, punch a little flat
    6: (5, 4, 4, 3, 5),   # blame the Wi-Fi — funny, but works for a human couple too
    7: (5, 4, 5, 4, 4),   # reset button when she freezes — sharp, specific
    8: (5, 3, 5, 4, 4),   # update between us — clean vow, familiar turn
    9: (5, 4, 5, 5, 4),   # spare battery / long runtime — vow + machine + punch at the end
}

WEIGHTS = (5, 4, 3, 2, 1)


def score(idx):
    """Weighted rubric score for candidate idx (max 75)."""
    return sum(w * s for w, s in zip(WEIGHTS, RUBRIC[idx]))


def rank():
    """Return [(score, -len, idx)] sorted best-first; ties go to shorter."""
    scored = [(score(i), -len(CANDIDATES[i]), i) for i in range(len(CANDIDATES))]
    scored.sort(reverse=True)
    return scored


def main():
    ranked = rank()
    print("Ranked candidates:")
    for s, neglen, i in ranked:
        print(f"  {s:3d} pts  {len(CANDIDATES[i]):3d} chars  #{i + 1}: {CANDIDATES[i]}")

    winner_score, _neglen, winner_idx = ranked[0]
    winner = CANDIDATES[winner_idx]

    # Gate: one line, 1-160 chars, non-blank, UTF-8.
    assert MIN_CHARS <= len(winner) <= MAX_CHARS, "winner out of length gate"
    assert winner.strip() == winner and "\n" not in winner, "winner must be one clean line"
    winner.encode("utf-8")

    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(winner + "\n")

    print(f"\nWinner: candidate #{winner_idx + 1} ({winner_score} pts, {len(winner)} chars)")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
