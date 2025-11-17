#!/usr/bin/env python3
"""
Performance Test for POI Classifier with Large Datasets

This script tests the classifier performance on the new Japanese POI data
and provides comprehensive statistics about classification coverage.
"""

import pandas as pd
import time
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.poi_classifier import classify_poi


def test_classifier_performance(sample_size=10000):
    """Test classifier with a sample of the large dataset"""

    print("=" * 100)
    print("POI CLASSIFIER PERFORMANCE TEST")
    print("=" * 100)

    # Load sample data from the large dataset
    data_file = project_root / 'data' / 'cleaned_JP_POI_part1.csv'

    if not data_file.exists():
        print(f"❌ Data file not found: {data_file}")
        print("Please ensure cleaned_JP_POI_part1.csv exists in the data directory.")
        return

    print(f"\nLoading sample of {sample_size:,} records from: {data_file.name}")
    df_sample = pd.read_csv(data_file, nrows=sample_size)
    actual_size = len(df_sample)
    print(f"✓ Loaded {actual_size:,} records")

    # Test classification performance
    print(f"\nClassifying {actual_size:,} POI records...")
    start_time = time.time()

    df_sample['category'] = df_sample.apply(
        lambda row: classify_poi(row['POI_type'], row['POI']),
        axis=1
    )

    elapsed = time.time() - start_time
    rate = actual_size / elapsed

    print(f"✓ Classification completed in {elapsed:.2f} seconds")
    print(f"  Processing rate: {rate:,.0f} records/second")

    # Analyze results
    print("\n" + "=" * 100)
    print("CLASSIFICATION RESULTS")
    print("=" * 100)

    category_counts = df_sample['category'].value_counts().sort_values(ascending=False)

    print("\nCategory Distribution:")
    print("-" * 100)
    for category, count in category_counts.items():
        percentage = (count / actual_size) * 100
        bar_length = int(percentage / 2)
        bar = "█" * bar_length
        print(f"  {category:20}: {count:>8,} ({percentage:>6.2f}%) {bar}")
    print("-" * 100)
    print(f"  {'Total':20}: {actual_size:>8,}")

    # Coverage analysis
    categorized = len(df_sample[df_sample['category'] != 'other'])
    coverage = (categorized / actual_size) * 100
    print(f"\n✓ Classification Coverage: {categorized:,} / {actual_size:,} ({coverage:.2f}%)")

    # Analyze 'other' category if it exists
    other_count = len(df_sample[df_sample['category'] == 'other'])
    if other_count > 0:
        print(f"\n⚠ Uncategorized POIs: {other_count:,} ({other_count/actual_size*100:.2f}%)")
        print("  Top 10 uncategorized POI types:")
        other_df = df_sample[df_sample['category'] == 'other']
        top_other = other_df.groupby(['POI_type', 'POI']).size().sort_values(ascending=False).head(10)
        for (poi_type, poi), count in top_other.items():
            print(f"    {poi_type:20} | {poi:25} : {count:>6,}")

    # Show top POI types per category
    print("\n" + "=" * 100)
    print("TOP POI TYPES PER CATEGORY (Top 5)")
    print("=" * 100)

    for category in sorted(df_sample['category'].unique()):
        category_df = df_sample[df_sample['category'] == category]
        top_types = category_df.groupby(['POI_type', 'POI']).size().sort_values(ascending=False).head(5)

        print(f"\n{category.upper()} ({len(category_df):,} records):")
        print("-" * 100)
        for (poi_type, poi), count in top_types.items():
            percentage = (count / len(category_df)) * 100
            print(f"  {poi_type:20} | {poi:30} : {count:>8,} ({percentage:>5.2f}%)")

    # Performance projection
    print("\n" + "=" * 100)
    print("PERFORMANCE PROJECTION FOR FULL DATASET")
    print("=" * 100)

    total_records = 1_017_224  # Combined size of both datasets
    estimated_time = total_records / rate

    print(f"\nBased on current performance ({rate:,.0f} records/second):")
    print(f"  Total records in both datasets: {total_records:,}")
    print(f"  Estimated processing time: {estimated_time:.1f} seconds ({estimated_time/60:.1f} minutes)")

    print("\n" + "=" * 100)
    print("TEST COMPLETED SUCCESSFULLY!")
    print("=" * 100)

    return df_sample


if __name__ == "__main__":
    # Test with 10,000 records (adjust as needed)
    test_size = 10000

    if len(sys.argv) > 1:
        try:
            test_size = int(sys.argv[1])
        except ValueError:
            print("Usage: python test_classifier_performance.py [sample_size]")
            sys.exit(1)

    test_classifier_performance(test_size)
