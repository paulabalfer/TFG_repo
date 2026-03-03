#!/usr/bin/env python3
"""Extract BATCH_RESULTS_JSON from session transcript JSONL file."""
import json
import re
import sys

JSONL_PATH = "/home/kike/.claude/projects/-home-kike-Documents-VS-Projects-natacion-paula/6621760c-89ee-40f1-bbc3-da8534e77c64.jsonl"
OUTPUT_PATH = "/home/kike/Documents/VS Projects/natacion_paula/results/predictions_batches_0_4.json"

def extract_json_arrays(text):
    """Find all JSON arrays of predictions in text."""
    results = []
    # Look for BATCH_RESULTS_JSON: followed by a JSON array
    pattern = r'BATCH_RESULTS_JSON:\s*\n?\s*(\[[\s\S]*?\])'
    matches = re.findall(pattern, text)
    for m in matches:
        try:
            arr = json.loads(m)
            if isinstance(arr, list) and len(arr) > 0 and isinstance(arr[0], dict) and 'filename' in arr[0]:
                results.append(arr)
        except json.JSONDecodeError:
            continue
    return results

# Read all lines and search for BATCH_RESULTS_JSON
all_predictions = []
seen_filenames = set()

with open(JSONL_PATH, 'r') as f:
    for line_num, line in enumerate(f):
        if 'BATCH_RESULTS_JSON' not in line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue

        # Search in the full JSON string for the arrays
        line_text = json.dumps(obj)

        # The text in JSONL is escaped, so we need to unescape it
        # Try to find the content field that contains BATCH_RESULTS_JSON
        text_content = line  # raw line

        # Try multiple extraction approaches
        arrays = extract_json_arrays(text_content)

        # Also try with unescaped newlines
        unescaped = text_content.replace('\\n', '\n').replace('\\\"', '"')
        arrays.extend(extract_json_arrays(unescaped))

        for arr in arrays:
            # Deduplicate based on first filename
            key = arr[0]['filename']
            if key not in seen_filenames:
                seen_filenames.add(key)
                all_predictions.append(arr)
                print(f"Found batch with {len(arr)} images starting with {key}")

print(f"\nTotal unique batches found: {len(all_predictions)}")
print(f"Total unique images: {sum(len(a) for a in all_predictions)}")

# Now identify which batches are 0-4 based on the image numbers
# Batch 0 starts with IMG_1249, Batch 5 starts with IMG_1382
batches_0_4 = {}
for arr in all_predictions:
    first_img = arr[0]['filename']
    img_num = int(re.search(r'IMG_(\d+)', first_img).group(1))

    if img_num < 1276:  # Batch 0
        batches_0_4["0"] = arr
    elif img_num < 1304:  # Batch 1
        batches_0_4["1"] = arr
    elif img_num < 1330:  # Batch 2
        batches_0_4["2"] = arr
    elif img_num < 1356:  # Batch 3
        batches_0_4["3"] = arr
    elif img_num < 1382:  # Batch 4
        batches_0_4["4"] = arr

print(f"\nBatches 0-4 found: {sorted(batches_0_4.keys())}")
for k in sorted(batches_0_4.keys()):
    v = batches_0_4[k]
    print(f"  Batch {k}: {len(v)} images, first={v[0]['filename']}, last={v[-1]['filename']}")

with open(OUTPUT_PATH, 'w') as f:
    json.dump(batches_0_4, f, indent=2)

print(f"\nSaved to {OUTPUT_PATH}")
