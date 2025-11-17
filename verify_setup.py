"""
Simple verification script to test POI classification without pandas dependency.
This script reads the CSV manually and applies classification.
"""

import csv
from src.poi_classifier import classify_poi


def verify_setup():
    print("=" * 80)
    print("POI CLASSIFICATION - SETUP VERIFICATION")
    print("=" * 80)
    print()

    # Read the CSV file
    data_path = 'data/poi_data.csv'
    print(f"Reading data from: {data_path}")
    print()

    with open(data_path, 'r') as f:
        reader = csv.DictReader(f)
        pois = list(reader)

    print(f"Loaded {len(pois)} POI records")
    print()

    # Apply classification and display results
    print("Classification Results:")
    print("=" * 80)
    print(f"{'POI Type':<20} {'POI':<25} {'Lat/Long':<30} {'Category':<20}")
    print("-" * 80)

    category_counts = {}

    for poi in pois:
        poi_type = poi['POI_type']
        poi_name = poi['POI']
        lat = poi['latitude']
        lon = poi['longitude']

        # Classify
        category = classify_poi(poi_type, poi_name)

        # Count categories
        category_counts[category] = category_counts.get(category, 0) + 1

        # Display
        coords = f"({lat}, {lon})"
        print(f"{poi_type:<20} {poi_name:<25} {coords:<30} {category:<20}")

    print()
    print("Category Distribution:")
    print("=" * 80)
    total = len(pois)
    for category in sorted(category_counts.keys()):
        count = category_counts[category]
        percentage = (count / total) * 100
        print(f"{category:<20} : {count:3} records ({percentage:.1f}%)")

    print()
    print("=" * 80)
    print("VERIFICATION COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print()
    print("Next steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run Jupyter notebook: jupyter notebook notebooks/poi_classification.ipynb")
    print("3. Run full demo: python demo.py (requires pandas)")
    print()


if __name__ == "__main__":
    verify_setup()
