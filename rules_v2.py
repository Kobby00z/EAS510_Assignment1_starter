"""EAS 510 - Project 1 - Phase 2: the V2 rule set.

Rules 1-3 are kept exactly as in `rules.py`. Your job is to ADD Rule 4 that
targets the systematic weakness you diagnosed from results_v1_hard.txt.

Constraint: the rules' `out_of` weights must still sum to 100 so the Final
Score stays on a /100 scale (the format validator enforces "Final Score:
<s>/100" equals the sum of the block's rule scores).

Example split that keeps the original spirit: Rules 1-3 -> 25/25/40 and
Rule 4 -> 10 (or trim the losers more aggressively).
"""

import rules
import cv2

def rule1_metadata(target,input_path):
    result = rules.rule1_metadata(target,input_path)
    result["out_of"] = 25
    result["score"] = round(result["score"] * 25 /30)
    return result 

def rule2_histogram(target, input_path):
    result = rules.rule2_histogram(target, input_path)
    result["out_of"] = 25
    result["score"] = round(result["score"] * 25 / 30)
    return result


#: Import the original rules and append your new one.
RULES = (rule1_metadata, rule2_histogram,rules.rule3_template, "rule4_edges")


def rule4_edges(target, input_path):
    """TODO: replace with your Phase 2 rule that fixes the V1 weakness.

    Starter returns a no-op so the pipeline still runs before you implement it.
    Parity with rules.py rule dict: rule/name/fired/score/out_of/note/metric.
    """
    original = cv2.imread(target["path"],cv2.IMREAD_GRAYSCALE)
    suspect = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    original_edges = cv2.Canny(original, 100, 200)
    suspect_edges = cv2.Canny(suspect, 100, 200)
    height, width = original_edges.shape
    suspect_edges = cv2.resize(suspect_edges, (width, height))
    comparison = cv2.matchTemplate(original_edges, suspect_edges, cv2.TM_CCOEFF_NORMED)
    similarity = float(comparison.max())
    similarity = max(0.0, min(1.0, similarity))
    matched = similarity >= 0.4
    return {
        "rule": 4,
        "name": "Edges",
        "fired": matched,
        "score": round(10 * similarity) if matched else 0,
        "out_of": 10,
        "note": f"Edge similarity {similarity:.2f}",
        "metric": round(similarity, 3),
    }
