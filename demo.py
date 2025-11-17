"""
POI Classification Demo Script

This script demonstrates how to use the POI classifier to process
POI data and generate classified output.

Usage:
    python demo.py [input_file] [output_file]

Examples:
    python demo.py                                          # Uses default: data/poi_data.csv
    python demo.py data/cleaned_JP_POI_part1.csv           # Specify input file
    python demo.py data/poi_data.csv data/output.csv       # Specify input and output
"""

import pandas as pd
import os
import sys
from pathlib import Path
from src.poi_classifier import classify_poi


def main():
    # Show help if requested
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        print(__doc__)
        print("\nAvailable data files:")
        data_dir = Path('data')
        if data_dir.exists():
            for csv_file in sorted(data_dir.glob('*.csv')):
                if 'classified' not in csv_file.name:
                    file_size = csv_file.stat().st_size
                    if file_size > 1_000_000:
                        size_str = f"{file_size / 1_000_000:.1f} MB"
                    else:
                        size_str = f"{file_size / 1000:.1f} KB"
                    print(f"  • {csv_file} ({size_str})")
        sys.exit(0)

    # Parse command-line arguments
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'data/poi_data.csv'

    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        # Generate output filename based on input
        input_path = Path(input_file)
        output_file = str(input_path.parent / f"{input_path.stem}_classified{input_path.suffix}")

    print("=" * 80)
    print("POI CLASSIFICATION DEMO")
    print("=" * 80)
    print()

    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Error: Input file not found: {input_file}")
        print()
        print("Available data files:")
        data_dir = Path('data')
        if data_dir.exists():
            for csv_file in sorted(data_dir.glob('*.csv')):
                if 'classified' not in csv_file.name:
                    print(f"  • {csv_file}")
        print()
        print("Usage: python demo.py [input_file] [output_file]")
        sys.exit(1)

    # Load the data
    print(f"Input file:  {input_file}")
    print(f"Output file: {output_file}")
    print()
    print(f"Loading data from: {input_file}")

    try:
        df = pd.read_csv(input_file)
        print(f"✓ Loaded {len(df):,} POI records")
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        sys.exit(1)
    print()

    # Display original data
    print("Original Data (first 5 rows):")
    print("-" * 80)
    print(df.head())
    print()

    # Apply classification
    print("Applying classification...")
    import time
    start_time = time.time()

    df['category'] = df.apply(
        lambda row: classify_poi(row['POI_type'], row['POI']),
        axis=1
    )

    elapsed = time.time() - start_time
    print(f"✓ Classification completed in {elapsed:.2f} seconds")
    if len(df) > 0:
        print(f"  Processing rate: {len(df)/elapsed:,.0f} records/second")
    print()

    # Show classified data
    print("Classified Data:")
    print("-" * 80)
    print(df.to_string(index=False))
    print()

    # Show statistics
    print("Category Distribution:")
    print("-" * 80)
    category_counts = df['category'].value_counts()
    for category, count in category_counts.items():
        percentage = (count / len(df)) * 100
        print(f"{category:20} : {count:3} ({percentage:.1f}%)")
    print()

    # Show examples by category
    print("Examples by Category:")
    print("=" * 80)
    for category in sorted(df['category'].unique()):
        print(f"\n{category.upper()}:")
        print("-" * 80)
        category_df = df[df['category'] == category][['POI_type', 'POI', 'latitude', 'longitude']]
        for _, row in category_df.iterrows():
            print(f"  • {row['POI_type']:20} | {row['POI']:20} | ({row['latitude']}, {row['longitude']})")

    print()

    # Save classified data
    df.to_csv(output_file, index=False)
    print(f"✓ Classified data saved to: {output_file}")
    print(f"  Total records: {len(df):,}")
    print()

    # Summary statistics
    print("Summary Statistics:")
    print("=" * 80)
    summary = df.groupby('category').agg({
        'POI': 'count',
        'latitude': ['min', 'max', 'mean'],
        'longitude': ['min', 'max', 'mean']
    }).round(6)
    summary.columns = ['Count', 'Min_Lat', 'Max_Lat', 'Avg_Lat', 'Min_Lon', 'Max_Lon', 'Avg_Lon']
    print(summary)
    print()

    print("=" * 80)
    print("DEMO COMPLETED SUCCESSFULLY!")
    print("=" * 80)


if __name__ == "__main__":
    main()
