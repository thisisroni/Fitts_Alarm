#!/usr/bin/env python3
"""Analyze Fitts Alarm CSV data and generate the report scatter plot."""

import csv
import html
import math
import statistics
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "fitts_alarm_results.csv"
OUTPUT_PATH = ROOT / "assets" / "fitts_law_scatter.svg"


def load_trials():
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as source:
        trials = list(csv.DictReader(source))

    for trial in trials:
        trial["A"] = float(trial["A"])
        trial["W"] = float(trial["W"])
        trial["MT"] = float(trial["MT"])
        trial["ID"] = math.log2(trial["A"] / trial["W"] + 1)
    return trials


def linear_regression(trials):
    x_values = [trial["ID"] for trial in trials]
    y_values = [trial["MT"] for trial in trials]
    x_mean = statistics.mean(x_values)
    y_mean = statistics.mean(y_values)
    slope = sum(
        (x - x_mean) * (y - y_mean) for x, y in zip(x_values, y_values)
    ) / sum((x - x_mean) ** 2 for x in x_values)
    intercept = y_mean - slope * x_mean
    predictions = [intercept + slope * x for x in x_values]
    residual_sum = sum((y - prediction) ** 2 for y, prediction in zip(y_values, predictions))
    total_sum = sum((y - y_mean) ** 2 for y in y_values)
    r_squared = 1 - residual_sum / total_sum
    return intercept, slope, r_squared


def make_svg(trials, intercept, slope, r_squared):
    width, height = 1000, 650
    left, right, top, bottom = 95, 955, 90, 555
    x_min, x_max = 1.0, 4.0
    y_min, y_max = 450.0, 1250.0

    def sx(value):
        return left + (value - x_min) / (x_max - x_min) * (right - left)

    def sy(value):
        return bottom - (value - y_min) / (y_max - y_min) * (bottom - top)

    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">Movement Time vs. Index of Difficulty</title>',
        '<desc id="desc">Scatter plot of 36 Fitts Alarm trials with a linear regression line.</desc>',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#172033}.grid{stroke:#d8dee9;stroke-width:1}.axis{stroke:#172033;stroke-width:2}.tick{font-size:14px}.label{font-size:18px;font-weight:600}.title{font-size:25px;font-weight:700}.subtitle{font-size:14px;fill:#536174}.point{fill:#2563eb;fill-opacity:.68;stroke:#174ea6;stroke-width:1}.fit{stroke:#dc2626;stroke-width:3}.legend{font-size:14px}</style>',
        '<text class="title" x="500" y="37" text-anchor="middle">Movement Time vs. Index of Difficulty</text>',
        '<text class="subtitle" x="500" y="61" text-anchor="middle">Fitts Alarm experiment · n = 36 trials</text>',
    ]

    for y_tick in range(500, 1201, 100):
        y_pos = sy(y_tick)
        elements.append(f'<line class="grid" x1="{left}" y1="{y_pos:.2f}" x2="{right}" y2="{y_pos:.2f}"/>')
        elements.append(f'<text class="tick" x="{left - 14}" y="{y_pos + 5:.2f}" text-anchor="end">{y_tick}</text>')

    for x_tick in [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]:
        x_pos = sx(x_tick)
        elements.append(f'<line class="grid" x1="{x_pos:.2f}" y1="{top}" x2="{x_pos:.2f}" y2="{bottom}"/>')
        elements.append(f'<text class="tick" x="{x_pos:.2f}" y="{bottom + 27}" text-anchor="middle">{x_tick:.1f}</text>')

    elements.extend([
        f'<line class="axis" x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}"/>',
        f'<line class="axis" x1="{left}" y1="{top}" x2="{left}" y2="{bottom}"/>',
        f'<text class="label" x="{(left + right) / 2}" y="618" text-anchor="middle">Index of Difficulty, ID (bits)</text>',
        f'<text class="label" x="27" y="{(top + bottom) / 2}" text-anchor="middle" transform="rotate(-90 27 {(top + bottom) / 2})">Movement Time, MT (ms)</text>',
    ])

    line_x1, line_x2 = min(t["ID"] for t in trials), max(t["ID"] for t in trials)
    line_y1, line_y2 = intercept + slope * line_x1, intercept + slope * line_x2
    elements.append(
        f'<line class="fit" x1="{sx(line_x1):.2f}" y1="{sy(line_y1):.2f}" x2="{sx(line_x2):.2f}" y2="{sy(line_y2):.2f}"/>'
    )

    for trial in trials:
        tooltip = html.escape(
            f'Trial {trial["trial"]}: A={trial["A"]:.0f}px, W={trial["W"]:.0f}px, '
            f'ID={trial["ID"]:.3f} bits, MT={trial["MT"]:.1f}ms'
        )
        elements.append(
            f'<circle class="point" cx="{sx(trial["ID"]):.2f}" cy="{sy(trial["MT"]):.2f}" r="6"><title>{tooltip}</title></circle>'
        )

    elements.extend([
        '<rect x="112" y="105" width="310" height="90" rx="8" fill="#ffffff" stroke="#b8c2d1"/>',
        f'<text class="legend" x="130" y="134">Linear model: MT = {intercept:.2f} + {slope:.2f} × ID</text>',
        f'<text class="legend" x="130" y="159">R² = {r_squared:.3f}</text>',
        '<circle class="point" cx="137" cy="180" r="5"/><text class="legend" x="151" y="185">Individual trial</text>',
        '<line class="fit" x1="274" y1="180" x2="308" y2="180"/><text class="legend" x="318" y="185">Linear fit</text>',
        '</svg>',
    ])
    OUTPUT_PATH.write_text("\n".join(elements), encoding="utf-8")


def main():
    trials = load_trials()
    intercept, slope, r_squared = linear_regression(trials)
    make_svg(trials, intercept, slope, r_squared)
    print(f"n={len(trials)}")
    print(f"a={intercept:.4f} ms")
    print(f"b={slope:.4f} ms/bit")
    print(f"R^2={r_squared:.6f}")
    print(f"plot={OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
