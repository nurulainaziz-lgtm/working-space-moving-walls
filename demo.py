"""
POI Classification Demo Script

This script demonstrates how to use the POI classifier to process
the sample data and generate classified output.
"""

import pandas as pd
import os
from src.poi_classifier import classify_poi


def main():
    print("=" * 80)
    print("POI CLASSIFICATION DEMO")
    print("=" * 80)
    print()

    # Load the data
    data_path = 'data/poi_data.csv'
    print(f"Loading data from: {data_path}")
    df = pd.read_csv(data_path)
    print(f"Loaded {len(df)} POI records")
    print()

    # Display original data
    print("Original Data (first 5 rows):")
    print("-" * 80)
    print(df.head())
    print()

    # Apply classification
    print("Applying classification...")
    df['category'] = df.apply(
        lambda row: classify_poi(row['POI_type'], row['POI']),
        axis=1
    )
    print("Classification completed!")
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
    output_path = 'data/poi_data_classified.csv'
    df.to_csv(output_path, index=False)
    print(f"Classified data saved to: {output_path}")
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
