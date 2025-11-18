# Popular Times Trend Analysis

## Overview

This analysis uses **machine learning clustering** to identify distinct popular times patterns across different stores. The **silhouette method** is used to determine the optimal number of trend clusters in your data.

## What This Analysis Does

1. **Loads Popular Times Data**: Reads hourly traffic patterns for each store across all days of the week
2. **Performs Clustering**: Groups stores with similar popular times patterns together
3. **Determines Optimal Clusters**: Uses the silhouette method to find the best number of trend groups
4. **Visualizes Patterns**: Creates comprehensive visualizations showing:
   - Silhouette scores for different cluster numbers
   - Hourly traffic patterns for each cluster
   - Store groupings in 2D space (PCA)
   - Correlation heatmaps between stores

## Data Format

Your data should be in CSV format with the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| `hour` | Hour of day (0-23) | 0, 1, 2, ..., 23 |
| `Reference_Id` | Unique store identifier | 804, 2192 |
| `Location` | Store name/location | "セブンイレブン池袋北口平和通り 7-eleven" |
| `Day` | Day of the week | Monday, Tuesday, ..., Sunday |
| `Ratio` | Raw popularity ratio | 0.45, 0.78 |
| `Adjusted_ratio` | Adjusted popularity ratio | 0.45, 0.78 |

## Files Created

- **`notebooks/popular_times_clustering.ipynb`**: Main analysis notebook
- **`data/popular_times.csv`**: Sample input data with 2 stores
- **`data/cluster_assignments.csv`**: Output file with cluster assignments for each store

## How to Use

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare Your Data

Place your popular times data in `data/popular_times.csv` with the format described above.

Sample data is already included with:
- **Store 804**: セブンイレブン池袋北口平和通り 7-eleven
- **Store 2192**: セブンイレブン浜野 7-eleven

### 3. Run the Notebook

```bash
jupyter notebook notebooks/popular_times_clustering.ipynb
```

Or if using JupyterLab:

```bash
jupyter lab notebooks/popular_times_clustering.ipynb
```

### 4. Execute All Cells

Run all cells in sequence to:
1. Load and preprocess the data
2. Perform silhouette analysis
3. Determine optimal number of clusters
4. Visualize trends and patterns
5. Generate cluster assignments

## Understanding the Results

### Silhouette Score

The **silhouette score** measures how well-defined your clusters are:

- **Score > 0.5**: Strong, well-separated clusters
- **Score 0.3-0.5**: Moderate cluster structure
- **Score < 0.3**: Weak or no substantial structure

### Cluster Interpretation

Each cluster represents a distinct **popular times pattern**:

- **Cluster 0**: Might represent "morning peak" stores
- **Cluster 1**: Might represent "evening peak" stores
- **Cluster 2**: Might represent "all-day steady" stores
- etc.

The notebook will automatically characterize each cluster by:
- Peak hour and value
- Lowest traffic hour
- Average traffic level
- Peak period (morning, afternoon, evening, night)

## Business Applications

Use these clusters for:

1. **Staffing Optimization**: Schedule staff based on cluster patterns
2. **Inventory Management**: Stock items according to traffic patterns
3. **Marketing Campaigns**: Time promotions based on cluster characteristics
4. **Store Grouping**: Group stores with similar patterns for operational decisions
5. **Performance Benchmarking**: Compare stores within the same cluster

## Key Visualizations

### 1. Silhouette Score Plot
Shows how the clustering quality changes with different numbers of clusters. The optimal number is marked with a red line.

### 2. Elbow Curve
Shows the within-cluster variance. Helps confirm the optimal number of clusters.

### 3. Cluster Pattern Plots
For each cluster, shows:
- Individual store patterns (gray lines)
- Average cluster pattern (colored line with markers)

### 4. PCA Visualization
Shows stores plotted in 2D space, colored by cluster. Stores that are close together have similar patterns.

### 5. Correlation Heatmap
Shows how strongly correlated stores are with each other. Stores in the same cluster should show high correlation.

## Technical Details

### Algorithms Used

1. **K-Means Clustering**: Groups stores based on hourly pattern similarity
2. **Silhouette Analysis**: Evaluates cluster quality for k=2 to k=10
3. **StandardScaler**: Normalizes features before clustering
4. **PCA**: Reduces dimensionality for visualization

### Feature Engineering

Each store is represented by a **24-dimensional feature vector**:
- One feature for each hour of the day
- Values are averaged across all days of the week
- Features are standardized (mean=0, std=1) before clustering

### Alternative Approaches

The notebook provides two feature engineering options:

1. **Hourly Features** (default): 24 features (hours 0-23 averaged across days)
2. **Day-Hour Features**: 168 features (24 hours × 7 days)

## Example Output

After running the analysis, you'll see:

```
Optimal number of clusters: 3
Best silhouette score: 0.6234

Cluster 0: 5 stores - Morning peak pattern
Cluster 1: 3 stores - Evening peak pattern
Cluster 2: 2 stores - All-day steady pattern
```

## Customization

### Adjust Maximum Clusters

In cell 8, change `max_clusters`:

```python
silhouette_results = perform_silhouette_analysis(X_scaled, max_clusters=15)
```

### Use Day-Hour Features

In cell 8, replace:

```python
X = hourly_features.fillna(0).values
```

with:

```python
X = feature_matrix.fillna(0).values
```

### Change Random Seed

For reproducible results, the random seed is set to 42. Change it in the KMeans calls:

```python
kmeans = KMeans(n_clusters=k, random_state=123, n_init=10)
```

## Troubleshooting

### Issue: "File not found"
**Solution**: Ensure `data/popular_times.csv` exists with the correct format

### Issue: "Not enough samples"
**Solution**: You need at least 3 stores to perform meaningful clustering

### Issue: "Poor silhouette scores"
**Solution**: Your data might not have distinct patterns. Try:
- Adding more stores
- Using day-hour features instead of hourly features
- Checking data quality

## Next Steps

1. Add more stores to your dataset for better pattern detection
2. Experiment with different clustering algorithms (DBSCAN, Hierarchical)
3. Add additional features (day type, weather, holidays)
4. Build predictive models based on cluster assignments

## Dependencies

- Python 3.7+
- pandas >= 1.3.0
- numpy >= 1.21.0
- scikit-learn >= 1.0.0
- matplotlib >= 3.4.0
- seaborn >= 0.11.0
- jupyter >= 1.0.0

## Support

For issues or questions, refer to:
- Jupyter documentation: https://jupyter.org/documentation
- scikit-learn clustering guide: https://scikit-learn.org/stable/modules/clustering.html
- Silhouette analysis: https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html
