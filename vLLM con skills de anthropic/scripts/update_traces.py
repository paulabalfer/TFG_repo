
import json
import os
import sys

def update_traces(new_traces_file):
    target_file = '/home/kike/Documents/VS Projects/natacion_paula/data/all_evaluation_traces.json'

    if os.path.exists(target_file):
        with open(target_file, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    with open(new_traces_file, 'r') as f:
        new_data = json.load(f)

    data.extend(new_data)

    with open(target_file, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Added {len(new_data)} traces. Total: {len(data)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        update_traces(sys.argv[1])
