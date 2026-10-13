# EAS 510 - Assignment 1: Digital Forensics Apprentice

A rule-based expert system that matches modified images back to their originals.

This is the **starter repository** for Project 1. Two repositories matter:

| Repository | Role |
|------------|------|
| `delveccj/EAS510_Assignment1_starter` (this repo) | Your **code** lives here. You will fork it, work in your fork, and push your final submission here. |
| `delveccj/EAS510_Assignment1` | The **dataset** (read-only). Clone it for the images; never commit it to your fork. |

## Setup on your Codio box

```bash
# 1. Fork this repo on GitHub, then in your box:
git clone https://github.com/YOUR-USERNAME/EAS510_Assignment1_starter.git
cd EAS510_Assignment1_starter

# 2. Clone the read-only dataset as a sibling folder (images live there):
cd ~/workspace
git clone https://github.com/delveccj/EAS510_Assignment1.git

# 3. Install dependencies:
cd ~/workspace/EAS510_Assignment1_starter
python3 -m pip install -r requirements.txt

# 4. Point this box at YOUR fork (run once):
./setup_git.sh
```

## Repository layout

```
forensics_detective.py   SimpleDetector: register targets + find_best_match
rules.py                 Rule functions (Rule 1: Metadata, Rule 2: Histogram, Rule 3: Template)
test_system.py           Runs the detector over the data folders and writes results_*.txt
scripts/check_output_format.py   Validates a results file against the required format
setup_git.sh, submit.sh  One-time setup + commit/push helper ("backup button")
```

## The task in one paragraph

Implement three interpretable rules (metadata, color histogram, template matching)
that combine into a 0-100 confidence score. Run your system on `modified_images/`
and `random/` and save the full output as `results_v1.txt`. In Phase 2, run on
`hard/`, diagnose a systematic failure, add a **Rule 4**, and save
`results_v1_hard.txt` and `results_v2.txt`. Full instructions are in the Codio guide
and in the assignment PDF in UBLearns.

## Running

```bash
# Phase 1 (easy + random) -> results_v1.txt
python3 test_system.py --modified --random --output results_v1.txt

# Phase 1 on hard cases -> results_v1_hard.txt
python3 test_system.py --hard --output results_v1_hard.txt

# Phase 2 (everything) -> results_v2.txt
python3 test_system.py --modified --hard --random --output results_v2.txt

# Validate any results file against the required format:
python3 scripts/check_output_format.py results_v1.txt
```

The data folders are resolved from a sibling clone of `EAS510_Assignment1`.
If your data is elsewhere, pass `--data-dir /path/to/EAS510_Assignment1`.

## Output format (do not alter)

```
Processing: modified_image_01.jpg
Rule 1 (Metadata): FIRED - Size ratio 0.85 -> 20/30 points
Rule 2 (Histogram): FIRED - Correlation 0.92 -> 25/30 points
Rule 3 (Template): FIRED - Match score 0.76 -> 30/40 points
Final Score: 75/100 -> MATCH to original_03.jpg
```

## Backup doctrine

Your Codio box can be reset at any time. **Your fork on GitHub is the only safe
copy.** After every milestone run `./submit.sh "describe what you did"`. A box
restart never touches GitHub.

## License

Apache 2.0. See `LICENSE`.

## Observed weakness in V1: what failed and why
One problem was that the detector couldn't recognize images when too many changes were made to them at the same time. For example with rule 1, changes to the image's dimension makes it immediately harder to recognize. With rule 2, any change to brightness or contrast can cause differences even though it's the same original picture. The template matching rule also makes it harder to find a strong pattern to match when there's a crop to the image. An example would be the image original_02__crop_keep70__bright__compress__q40__v2.jpg. The filename says it was cropped to keep 70% of the image then made brighter and compressed. It was rejected because Rule 2 and Rule 3 failed to find strong matches even though rule 1 gave a high score of 29/30. To my naked eye the dimensions look similar enough to explain why Rule 1 returned a high score. The cropping removed the darker ground and people, leaving mainly the red building which changed the distribution of colors and where visual features appeared

## Design decision for V2: what Rule 4 is and why you chose it
Rule 4 is edge detection which was supposed to read the outlines of the images to see how similar they are. I chose this because changing brightness or contrast can affect the colors without affecting the outline of an image. I was hoping that rule 4 would spot some images that rule 2 could not.

## Effect of the change: accuracy before/after on easy vs hard
V1 accepted 58 out of 60 easy images as matches and 48 out of 60 hard images as matches. V2 accepted 56 out of 60 easy images as matches and 39 out of 60 hard images as matches. Both rejected all the random images. V2 performed worse than V1 especially on the hard images

## Trade-offs: what new costs or risks did Rule 4 introduce
The main cost of Rule 4 for me was the processing time as it took over thirty minutes to compare the edges.  V2 also showed fewer matches with the hard images than V1. Another potential problem is that an image being cropped may shift the outline or even make it disappear entirely which would render the rule less reliable than we would ideally want. An example for that is the same original_02__crop_keep70__bright__compress__q40__v2.jpg image which performed worse with V2 since it was cropped with some edges shifted and others disappeared.  With V1, it scored 29/100 and with V2, 24/100.  Rule 4 was 0/10.