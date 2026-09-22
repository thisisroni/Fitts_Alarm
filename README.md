# Fitts Alarm: An Anti-Snooze Clicking Experiment

Fitts Alarm is an interactive web experiment that combines an anti-snooze alarm scenario with data collection based on Fitts' Law. Instead of dismissing the alarm with a single click in a fixed location, participants must click 36 circular targets that vary randomly in position and size. This interaction is designed to disrupt muscle memory while recording movement time (MT).

The entire project consists of a single `index.html` file. No framework, dependencies, or build steps are required, so it can be opened directly in a browser or deployed to GitHub Pages.

## Quick Start

1. Open `index.html` in a desktop browser.
2. Optionally enter a session label, such as `sleepy_01` or `awake_01`.
3. Read the instructions at the top of the page and click **「起床／開始解除鬧鐘」 (Wake Up / Start Dismissing Alarm)**.
4. Click each of the 36 circular targets in sequence.
5. When the experiment is complete, click **「下載 CSV 實驗資料」 (Download CSV Experiment Data)**.
6. To run another session, click **「再測一次」 (Run Again)**, update the label if needed, and restart the experiment.

For best results, use a desktop computer and mouse. Keep the browser zoom level, window size, input device, and sitting posture consistent across experimental conditions.

## How to Use Session Labels

The session label is an optional identifier for the experimental condition. It does not affect trial generation or timing. Use a consistent naming convention, such as:

| Example label | Meaning |
|---|---|
| `sleepy_01` | First measurement immediately after waking up |
| `awake_01` | First measurement while fully awake |
| `p03_sleepy` | Participant 3, immediately after waking up |

The label is stored in the CSV `session` column and included in the downloaded filename, for example, `fitts_alarm_results_sleepy_01.csv`. The label field is temporarily locked after the experiment begins. Selecting **「再測一次」 (Run Again)** unlocks the field while preserving its current value.

## Experiment Design

| Factor | Levels |
|---|---|
| Target Distance A | 150, 300, and 450 px |
| Target Width W (circle diameter) | 40, 70, and 100 px |
| Repetitions per combination | 4 |
| Total trials | 3 × 3 × 4 = 36 |

- Each of the nine `(A, W)` combinations appears four times. Trials are randomized at the start using a Fisher-Yates shuffle.
- For the first target, distance is measured from the actual position where the start button was clicked. For every subsequent target, it is measured from the actual position of the previous successful click.
- The distance between the starting point and the target center is exactly equal to the trial's A value, and the entire circle remains within the 900 × 700 canvas.
- Clicking outside the target increments that trial's `misses` count. It does not advance to the next target or reset the timer.

## Timing

The app uses `performance.now()` for timing:

- First MT: measured from clicking the start button to successfully hitting the first target.
- Subsequent MTs: measured from successfully hitting the previous target to successfully hitting the current target.
- If a miss occurs, the MT includes the time spent retrying.
- MT is measured in milliseconds and recorded to one decimal place.

## CSV Data

Each row in the CSV represents one trial:

```csv
trial,A,W,MT,misses,session
1,300,70,612.4,0,sleepy_01
2,150,40,845.1,1,sleepy_01
```

| Column | Description |
|---|---|
| `trial` | Trial number, starting from 1 |
| `A` | Target distance (px) |
| `W` | Target diameter (px) |
| `MT` | Movement time (ms) |
| `misses` | Number of missed clicks before the successful hit |
| `session` | Session label entered by the user |

During the experiment, data is stored only in the current browser tab's memory. Download the CSV after completing a session. If you try to start another session before downloading the results, the app will display a warning. Refreshing or closing the tab also clears any results that have not been downloaded.

## Deploying to GitHub Pages

1. Place `index.html` and this README in the root directory of the GitHub repository.
2. Open **Settings → Pages** in the repository.
3. Set **Source** to **Deploy from a branch**.
4. Select the branch to deploy—usually `main`—and choose `/ (root)`.
5. Save the settings and wait for GitHub to provide the website URL.

This project does not require a backend. The browser generates the CSV locally using a `Blob` and a temporary download link.

## Adjusting Experiment Parameters

The following constants can be modified in the JavaScript section of `index.html`:

```js
const DISTANCES = [150, 300, 450];
const WIDTHS = [40, 70, 100];
const REPETITIONS = 4;
```

If you increase the maximum distance or target size, verify that the full target can still be placed within the 900 × 700 canvas from every possible starting point. Otherwise, the specified A value may no longer be accurate.

## Project Structure

```text
Fitts_Alarm/
├── index.html   # Complete app: layout, canvas, experiment logic, and CSV export
└── README.md    # Usage, data, and deployment documentation
```
