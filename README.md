# Data Engineering Projects

This repository contains data engineering projects for POI classification and store impression analysis.

## Project Structure

```
working-space-moving-walls/
├── data/
│   ├── poi_data.csv                      # Original POI data
│   ├── poi_data_classified.csv           # Classified POI data (generated)
│   ├── store_impression_data.csv         # Store daily impression data
│   ├── store_clustering_results.csv      # Clustering results (generated)
│   └── store_correlation_matrix.csv      # Store correlation matrix (generated)
├── notebooks/
│   ├── poi_classification.ipynb          # POI classification notebook
│   └── store_impression_analysis.ipynb   # Store impression analysis notebook
├── src/
│   ├── __init__.py
│   └── poi_classifier.py                 # Core classification module
├── output/
│   └── quick_clustering_results.csv      # Quick analysis results (generated)
├── requirements.txt                      # Python dependencies
├── run_store_analysis.py                 # Quick store analysis script
├── demo.py                               # Demo script
└── README.md                             # This file
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Jupyter Notebook

```bash
cd notebooks
jupyter notebook poi_classification.ipynb
```

### 3. Use the Classifier Module

```python
from src.poi_classifier import classify_poi

# Classify a single POI
category = classify_poi('amenity', 'restaurant')
print(category)  # Output: business
```

### 4. Run Store Impression Analysis

#### Quick Analysis (Command Line)
```bash
python run_store_analysis.py
```

#### Full Analysis (Jupyter Notebook)
```bash
cd notebooks
jupyter notebook store_impression_analysis.ipynb
```

---

## Project 1: POI Data Classification

### POI Categories

The system classifies POIs into four main categories:

### 1. **Business**
Commercial establishments and services:
- Shops (convenience stores, supermarkets, etc.)
- Restaurants, cafes, pubs, bars
- Banks, pharmacies

### 2. **Tourism**
Tourism-related facilities:
- Hotels, guest houses, motels
- Information centers
- Museums, attractions, viewpoints

### 3. **Public Services**
Government and community services:
- Police stations
- Post offices
- Places of worship
- Schools, universities, libraries
- Hospitals, clinics
- Social facilities

### 4. **Transportation**
Transportation infrastructure:
- Traffic signals, crossings
- Ferry terminals, bus stations
- Public transport platforms

## Data Format

### Input Data (poi_data.csv)
```csv
POI_type,POI,latitude,longitude
highway,traffic_signals,24.4519523,122.9439556
amenity,police,24.4511259,122.9459816
```

### Output Data (poi_data_classified.csv)
```csv
POI_type,POI,latitude,longitude,category
highway,traffic_signals,24.4519523,122.9439556,transportation
amenity,police,24.4511259,122.9459816,public_services
```

## Classification Logic

The classifier uses a priority-based approach:

1. **Tourism** (highest priority) - Direct tourism-related POIs
2. **Transportation** - Infrastructure for movement
3. **Public Services** - Government and community services
4. **Business** - Commercial establishments
5. **Fallback** - Based on POI_type if no specific match found

## Usage Examples

### Classify from CSV using pandas

```python
import pandas as pd
from src.poi_classifier import classify_poi

# Load data
df = pd.read_csv('data/poi_data.csv')

# Apply classification
df['category'] = df.apply(
    lambda row: classify_poi(row['POI_type'], row['POI']),
    axis=1
)

# Save results
df.to_csv('data/poi_data_classified.csv', index=False)
```

### Analyze distribution

```python
# Count by category
category_counts = df['category'].value_counts()
print(category_counts)

# Percentage distribution
percentages = (df['category'].value_counts(normalize=True) * 100).round(2)
print(percentages)
```

## Features

- **Comprehensive classification rules** covering common POI types
- **Extensible design** - Easy to add new categories or POI types
- **Jupyter notebook** with full analysis workflow
- **Reusable module** for integration into other projects
- **Detailed documentation** and examples

## Development

### Adding New POI Types

Edit `src/poi_classifier.py` and add the new POI to the appropriate category dictionary:

```python
business_pois = {
    'shop': ['convenience', 'supermarket', 'your_new_type'],
    'amenity': ['restaurant', 'cafe']
}
```

### Testing

Run the module directly to test:

```bash
python src/poi_classifier.py
```

---

## Project 2: Store Impression Analysis

### Overview

This project analyzes store impression data to identify patterns, correlations, and groupings among stores based on their daily impression metrics.

### Features

- **Correlation Analysis**: Calculate correlations between stores based on impression patterns
- **K-Means Clustering**: Group stores with similar impression patterns
- **Silhouette Score Analysis**: Evaluate clustering quality per store
- **Hierarchical Clustering**: Visualize store relationships via dendrograms
- **Comprehensive Visualizations**: Heatmaps, scatter plots, box plots, and more

### Data Format

#### Input Data (store_impression_data.csv)
```csv
f0_,zo_name,do_cd,do_name,store_cd,store_name_kanji,f1_,FileName
11/3/2024,京浜,244,目黒,358859,目黒元競馬場,925,[秘B関係者限]京浜
```

**Column Mapping:**
- `f0_` → date
- `do_cd` → district code
- `store_cd` → unique store identifier
- `f1_` → daily_impression (daily impression count)

### Quick Start

#### Option 1: Quick Command-Line Analysis
```bash
python run_store_analysis.py
```

This will:
- Load store impression data
- Calculate store correlations
- Perform K-Means clustering
- Calculate silhouette scores per store
- Save results to `output/` directory

#### Option 2: Full Jupyter Notebook Analysis
```bash
cd notebooks
jupyter notebook store_impression_analysis.ipynb
```

The notebook provides:
- Interactive data exploration
- Detailed correlation analysis
- Clustering with optimal K selection
- Silhouette score visualization
- Cluster profiling and interpretation
- Export of all results

### Output Files

The analysis generates the following files:

- `store_clustering_results.csv` - Stores with cluster assignments and silhouette scores
- `store_correlation_matrix.csv` - Pairwise correlation matrix between stores
- `store_pairs_correlation.csv` - All store pairs with correlation values
- `cluster_profiles.csv` - Statistical profiles of each cluster

### Key Metrics

1. **Silhouette Score**: Measures how well each store fits its assigned cluster
   - Range: [-1, 1]
   - > 0.5: Well-clustered
   - 0.25 - 0.5: Moderate clustering
   - < 0.25: Weak clustering
   - < 0: Potentially misclassified

2. **Correlation**: Measures similarity in impression patterns between stores
   - Range: [-1, 1]
   - Close to 1: Similar patterns
   - Close to -1: Opposite patterns
   - Close to 0: No relationship

3. **Coefficient of Variation (CV)**: Measures relative variability
   - CV = std / mean
   - Higher CV indicates more variable impression patterns

### Analysis Workflow

1. **Data Loading**: Load and validate store impression data
2. **Preprocessing**: Create pivot tables, handle missing values
3. **Correlation Analysis**: Calculate pairwise correlations between stores
4. **Feature Engineering**: Create aggregate metrics per store
5. **Clustering**: Apply K-Means with optimal K selection
6. **Silhouette Analysis**: Calculate scores to evaluate clustering quality
7. **Visualization**: Generate plots to interpret results
8. **Export**: Save all results for further analysis

### Example Use Cases

- Identify stores with similar performance patterns
- Find optimal store groupings for targeted strategies
- Detect outlier stores that don't fit common patterns
- Understand geographical or operational similarities
- Support decision-making for store management

---

## Requirements

- Python 3.7+
- pandas >= 1.3.0
- numpy >= 1.21.0
- jupyter >= 1.0.0
- notebook >= 6.4.0
- matplotlib >= 3.4.0
- seaborn >= 0.11.0
- scikit-learn >= 0.24.0
- scipy >= 1.7.0

## License

This project is for educational and demonstration purposes.

## Contributing

Feel free to extend the classification rules or add new features!
