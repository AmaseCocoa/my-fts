import csv
import sys
from pathlib import Path

from src import SimpleFTS

def build_index(csv_path: str = "./data/13TOKYO.CSV", index_path: str = "./index.msgpack") -> None:
    """Build and save FTS index."""
    fts = SimpleFTS()
    csv_file_path = Path(csv_path)
    
    print(f"Reading {csv_file_path}...")
    with open(csv_file_path, "r", encoding="shift_jis") as f:
        reader = csv.reader(f)
        count = 0
        for row in reader:
            zip_code = row[2]
            pref = row[6]
            city = row[7]
            town = row[8]

            if town != "以下に掲載がない場合":
                full_text = f"{zip_code} {pref}{city}{town}"
                fts.add_index(full_text)
                count += 1
        
        print(f"Indexed {count} entries")
    
    print(f"Saving to {index_path}...")
    fts.save(index_path)
    print("✓ Index saved successfully")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        build_index(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "./index.msgpack")
    else:
        build_index()