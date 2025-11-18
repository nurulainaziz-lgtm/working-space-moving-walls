#!/usr/bin/env python
"""
Quick Demo: Store Impression Correlation and Silhouette Analysis

This script provides a quick demonstration of the store analysis workflow.
For full analysis, please use the Jupyter notebook: notebooks/store_impression_analysis.ipynb

Usage:
    python run_store_analysis.py
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for server environments
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, silhouette_samples
import os
import warnings
warnings.filterwarnings('ignore')

def main():
    print("="*80)
    print("STORE IMPRESSION CORRELATION AND SILHOUETTE ANALYSIS - QUICK DEMO")
    print("="*80)

    # Load data
    print("\n1. Loading data...")
    data_path = 'data/store_impression_data.csv'
    df = pd.read_csv(data_path)
    df.rename(columns={'f0_': 'date', 'f1_': 'daily_impression'}, inplace=True)
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')

    print(f"   ✓ Loaded {len(df)} records")
    print(f"   ✓ Date range: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
    print(f"   ✓ Number of unique stores: {df['store_cd'].nunique()}")
    print(f"   ✓ Average daily impression: {df['daily_impression'].mean():.0f}")

    # Create pivot table
    print("\n2. Creating store-date impression matrix...")
    store_impression_pivot = df.pivot_table(
        index='store_cd',
        columns='date',
        values='daily_impression',
        aggfunc='sum'
    ).fillna(0)
    print(f"   ✓ Matrix shape: {store_impression_pivot.shape}")

    # Calculate correlations
    print("\n3. Calculating store correlations...")
    store_correlation = store_impression_pivot.T.corr()
    corr_values = store_correlation.values[np.triu_indices_from(store_correlation.values, k=1)]
    print(f"   ✓ Average correlation: {corr_values.mean():.4f}")
    print(f"   ✓ Max correlation: {corr_values.max():.4f}")
    print(f"   ✓ Min correlation: {corr_values.min():.4f}")

    # Clustering
    print("\n4. Performing K-Means clustering...")
    X = store_impression_pivot.values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Find optimal K
    max_k = min(6, len(X_scaled))
    K_range = range(2, max_k)
    silhouette_scores = []

    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X_scaled)
        silhouette_scores.append(silhouette_score(X_scaled, labels))

    optimal_k = K_range[np.argmax(silhouette_scores)]
    print(f"   ✓ Optimal number of clusters: {optimal_k}")
    print(f"   ✓ Maximum silhouette score: {max(silhouette_scores):.4f}")

    # Final clustering with optimal K
    print("\n5. Computing final clustering results...")
    kmeans_optimal = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
    cluster_labels = kmeans_optimal.fit_predict(X_scaled)
    silhouette_vals = silhouette_samples(X_scaled, cluster_labels)

    # Create results dataframe
    clustering_results = pd.DataFrame({
        'store_cd': store_impression_pivot.index,
        'cluster': cluster_labels,
        'silhouette_score': silhouette_vals
    })

    # Merge with store info
    store_metadata = df[['store_cd', 'store_name_kanji', 'do_name']].drop_duplicates()
    clustering_results = clustering_results.merge(store_metadata, on='store_cd', how='left')

    # Calculate store features
    store_features = df.groupby('store_cd').agg({
        'daily_impression': ['mean', 'sum']
    }).reset_index()
    store_features.columns = ['store_cd', 'avg_impression', 'total_impression']
    clustering_results = clustering_results.merge(store_features, on='store_cd', how='left')

    print(f"   ✓ Overall silhouette score: {silhouette_score(X_scaled, cluster_labels):.4f}")
    print(f"   ✓ Stores with negative silhouette: {len(clustering_results[clustering_results['silhouette_score'] < 0])}")

    # Display results
    print("\n6. CLUSTERING RESULTS:")
    print("="*80)
    for cluster in range(optimal_k):
        cluster_data = clustering_results[clustering_results['cluster'] == cluster]
        print(f"\nCluster {cluster}:")
        print(f"   - Number of stores: {len(cluster_data)}")
        print(f"   - Avg impression: {cluster_data['avg_impression'].mean():.0f}")
        print(f"   - Avg silhouette score: {cluster_data['silhouette_score'].mean():.4f}")
        print(f"   - Top 3 stores (by silhouette score):")
        top_stores = cluster_data.nlargest(3, 'silhouette_score')
        for idx, row in top_stores.iterrows():
            print(f"      • {row['store_name_kanji']} (Score: {row['silhouette_score']:.4f}, Avg Impression: {row['avg_impression']:.0f})")

    # Save results
    print("\n7. Saving results...")
    os.makedirs('output', exist_ok=True)

    output_path = 'output/quick_clustering_results.csv'
    clustering_results.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"   ✓ Clustering results saved to: {output_path}")

    corr_path = 'output/quick_correlation_matrix.csv'
    store_correlation.to_csv(corr_path, encoding='utf-8-sig')
    print(f"   ✓ Correlation matrix saved to: {corr_path}")

    print("\n" + "="*80)
    print("ANALYSIS COMPLETE!")
    print("="*80)
    print("\nFor detailed analysis with visualizations, please run:")
    print("   jupyter notebook notebooks/store_impression_analysis.ipynb")
    print("="*80)

if __name__ == "__main__":
    main()
